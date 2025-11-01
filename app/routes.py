import math
import os
from flask import Blueprint, render_template, request, jsonify, current_app
from .database import MGNREGADatabase
from .terminology import terminology, translations
import google.generativeai as genai

main = Blueprint('main', __name__)

# Global database instance
db = None

def get_db():
    global db
    if db is None:
        db = MGNREGADatabase(current_app.config['DATABASE_PATH'])
    return db

# Karnataka district coordinates (approximate centers) - mapped to database names
KARNATAKA_DISTRICTS = [
    {'district': 'BENGALURU', 'latitude': 12.9716, 'longitude': 77.5946},  # Maps to Bengaluru Urban
    {'district': 'BENGALURU RURAL', 'latitude': 13.0827, 'longitude': 77.5876},
    {'district': 'MYSURU', 'latitude': 12.2958, 'longitude': 76.6394},
    {'district': 'BELAGAVI', 'latitude': 15.8497, 'longitude': 74.4977},
    {'district': 'MANDYA', 'latitude': 12.5223, 'longitude': 76.8976},
    {'district': 'TUMAKURU', 'latitude': 13.3409, 'longitude': 77.1013},
    {'district': 'BALLARI', 'latitude': 15.1394, 'longitude': 76.9214},
    {'district': 'DAVANAGERE', 'latitude': 14.4644, 'longitude': 75.9218},
    {'district': 'SHIVAMOGGA', 'latitude': 13.9299, 'longitude': 75.5681},
    {'district': 'UDUPI', 'latitude': 13.3409, 'longitude': 74.7421},
    {'district': 'CHIKKAMAGALURU', 'latitude': 13.3153, 'longitude': 75.7754},
    {'district': 'DAKSHINA KANNADA', 'latitude': 12.8435, 'longitude': 75.2479},
    {'district': 'UTTARA KANNADA', 'latitude': 14.6667, 'longitude': 74.5000},
    {'district': 'HASSAN', 'latitude': 13.0068, 'longitude': 76.0996},
    {'district': 'CHITRADURGA', 'latitude': 14.2266, 'longitude': 76.4006},
    {'district': 'KODAGU', 'latitude': 12.3375, 'longitude': 75.8069},
    {'district': 'KOLAR', 'latitude': 13.1367, 'longitude': 78.1292},
    {'district': 'CHIKKABALLAPURA', 'latitude': 13.4355, 'longitude': 77.7315},
    {'district': 'RAMANAGARA', 'latitude': 12.7150, 'longitude': 77.2809},
    {'district': 'YADGIR', 'latitude': 16.7700, 'longitude': 77.1376},
    {'district': 'RAICHUR', 'latitude': 16.2076, 'longitude': 77.3463},
    {'district': 'KOPPAL', 'latitude': 15.3500, 'longitude': 76.1500},
    {'district': 'GADAG', 'latitude': 15.4167, 'longitude': 75.6167},
    {'district': 'BAGALKOTE', 'latitude': 16.1833, 'longitude': 75.7000},
    {'district': 'VIJAYPURA', 'latitude': 16.8300, 'longitude': 75.7100},
    {'district': 'KALABURAGI', 'latitude': 17.3297, 'longitude': 76.8343},
    {'district': 'BIDAR', 'latitude': 17.9133, 'longitude': 77.5300},
    {'district': 'DHARWAR', 'latitude': 15.4589, 'longitude': 75.0078},
    {'district': 'HAVERI', 'latitude': 14.7950, 'longitude': 75.4000},
]

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula."""
    R = 6371  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def find_nearest_district(latitude, longitude):
    """Find the nearest district to given coordinates."""
    nearest_district = KARNATAKA_DISTRICTS[0]
    min_distance = calculate_distance(latitude, longitude, nearest_district['latitude'], nearest_district['longitude'])

    for district in KARNATAKA_DISTRICTS:
        distance = calculate_distance(latitude, longitude, district['latitude'], district['longitude'])
        if distance < min_distance:
            min_distance = distance
            nearest_district = district

    return {
        'district': nearest_district['district'],
        'distance': round(min_distance, 1)
    }

@main.route('/')
def dashboard():
    """Main dashboard page."""
    language = request.args.get('lang', 'kn')  # Default to Kannada for rural users
    selected_district = request.args.get('district', '')

    try:
        database = get_db()
        districts = database.get_districts()

        # Set default district if available
        if not selected_district and districts:
            selected_district = districts[0]

        current_data = None
        historical_data = []

        if selected_district:
            district_data = database.get_performance_by_district(selected_district)
            if district_data:
                # Sort by year and month
                district_data.sort(key=lambda x: (x.year, x.month))
                historical_data = [item.to_dict() for item in district_data]
                current_data = historical_data[-1] if historical_data else None

        # Convert terminology objects to dictionaries for JSON serialization
        terminology_dict = {key: term.to_dict(language) for key, term in terminology.items()}

        return render_template('dashboard.html',
                             language=language,
                             selected_district=selected_district,
                             districts=districts,
                             current_data=current_data,
                             historical_data=historical_data,
                             terminology=terminology_dict,
                             translations=translations)

    except Exception as e:
        print(f"Error loading dashboard: {e}")
        # Convert terminology objects to dictionaries for JSON serialization
        terminology_dict = {key: term.to_dict(language) for key, term in terminology.items()}
        return render_template('dashboard.html',
                             language=language,
                             selected_district=selected_district,
                             districts=[],
                             current_data=None,
                             historical_data=[],
                             terminology=terminology_dict,
                             translations=translations)

@main.route('/api/geolocation', methods=['POST'])
def geolocation():
    """API endpoint for geolocation-based district detection."""
    try:
        data = request.get_json()
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Invalid latitude or longitude'}), 400

        latitude = float(data['latitude'])
        longitude = float(data['longitude'])

        # Check if coordinates are within Karnataka bounds (approximate)
        karnataka_bounds = {
            'north': 18.5,
            'south': 11.5,
            'east': 78.6,
            'west': 74.0
        }

        if (latitude < karnataka_bounds['south'] or latitude > karnataka_bounds['north'] or
            longitude < karnataka_bounds['west'] or longitude > karnataka_bounds['east']):
            return jsonify({'error': 'Location appears to be outside Karnataka'}), 400

        nearest = find_nearest_district(latitude, longitude)

        # Check if the district has data in our database
        database = get_db()
        available_districts = database.get_districts()
        has_data = nearest['district'] in available_districts

        return jsonify({
            'district': nearest['district'],
            'distance': nearest['distance'],
            'hasData': has_data,
            'unit': 'km',
            'message': f"Nearest district {'with data: ' if has_data else ': '}{nearest['district']} ({nearest['distance']} km away){'' if has_data else ' - no data available'}"
        })

    except Exception as e:
        print(f"Geolocation error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/geolocation', methods=['GET'])
def get_districts():
    """Get list of available districts."""
    try:
        database = get_db()
        districts = database.get_districts()
        return jsonify({
            'districts': districts,
            'total': len(districts)
        })
    except Exception as e:
        print(f"Error fetching districts: {e}")
        return jsonify({'error': 'Failed to fetch districts'}), 500

@main.route('/api/generate-insights', methods=['POST'])
def generate_insights():
    """Generate AI-powered insights for district performance."""
    try:
        data = request.get_json()
        district = data.get('district')
        language = data.get('language', 'en')

        if not district:
            return jsonify({'error': 'District is required'}), 400

        # Get district data
        database = get_db()
        district_data = database.get_performance_by_district(district)

        if not district_data:
            return jsonify({'error': 'No data available for this district'}), 404

        # Prepare data for AI analysis
        latest_data = district_data[-1]  # Most recent data

        # Configure Gemini AI
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash-001')

        prompt = f"""
        Analyze the MGNREGA performance data for {district} district and provide insights in {'Kannada' if language == 'kn' else 'English'}.

        Current month data:
        - Person-days generated: {latest_data.person_days_generated} lakhs
        - Total expenditure: {latest_data.total_expenditure} crores
        - Average days of employment: {latest_data.avg_days_of_employment} days
        - Work completion rate: {latest_data.work_completion_rate}%
        - Households with 100 days work: {latest_data.total_households_completed_100_days}
        - Female participation rate: {latest_data.female_participation_rate}%

        Provide a structured analysis with:
        1. **Performance Summary**: A brief overview of current performance
        2. **Key Strengths**: What the district is doing well
        3. **Areas for Improvement**: Where there are challenges
        4. **Recommendations**: Simple, actionable suggestions

        IMPORTANT: Return ONLY the content to be displayed on a webpage. Do NOT include HTML document structure like <!DOCTYPE>, <html>, <head>, <body> tags.

        Use simple HTML formatting for display:
        - Use <strong> or <b> tags for emphasis
        - Use <br> for line breaks within paragraphs
        - Use <p> tags for paragraphs
        - Use <ul><li> for bullet points and <ol><li> for numbered lists
        - Use <h3> tags for section headings
        - Keep the language simple and easy to understand for rural citizens
        """

        response = model.generate_content(prompt)
        insights = response.text

        return jsonify({'insights': insights})

    except Exception as e:
        print(f"Error generating insights: {e}")
        return jsonify({'error': 'Failed to generate insights'}), 500
