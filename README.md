# MGNREGA Dashboard

A production-ready web application for visualizing Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) performance data for Karnataka districts. Built with Python Flask, this application provides citizens with easy access to government welfare program performance metrics.

## Features

- **District-wise Performance Data**: View MGNREGA performance metrics for all Karnataka districts
- **Interactive Dashboard**: Modern, responsive web interface with data visualizations
- **Multi-language Support**: English and Kannada (ಕನ್ನಡ) language options
- **Auto Location Detection**: Automatically detect user's district based on geolocation
- **AI-Powered Insights**: Generate intelligent summaries and recommendations using Google Gemini AI
- **Historical Data**: Compare performance across multiple months and years
- **Offline-Capable**: Cached data ensures reliability even when government APIs are down

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with connection pooling
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js for data visualization
- **Styling**: Tailwind CSS
- **AI**: Google Generative AI (Gemini)
- **Deployment**: Docker + Gunicorn

## Data Sources

- **Primary**: data.gov.in MGNREGA API
- **State**: Karnataka
- **Time Period**: Last 3 years of monthly performance data
- **Caching**: Local SQLite database for reliability

## Installation & Setup

### Prerequisites

- Python 3.11+
- SQLite3
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mgnrega-dashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Fetch initial data**
   ```bash
   python fetch_data.py
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   - Open http://localhost:5000 in your browser

### Production Deployment

#### Using Docker

1. **Build the Docker image**
   ```bash
   docker build -t mgnrega-dashboard .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     --name mgnrega-app \
     -p 5000:5000 \
     -v $(pwd)/mgnrega.db:/app/mgnrega.db \
     mgnrega-dashboard
   ```

#### Manual VPS Deployment

1. **Set up VPS (Ubuntu/Debian)**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and pip
   sudo apt install python3 python3-pip python3-venv sqlite3 -y

   # Install nginx
   sudo apt install nginx -y
   ```

2. **Deploy application**
   ```bash
   # Clone repository
   git clone <your-repo-url>
   cd mgnrega-dashboard

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Set up environment
   cp .env.example .env
   # Edit .env with production values

   # Fetch data
   python fetch_data.py

   # Run with Gunicorn
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:create_app()
   ```

3. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /path/to/your/app/static;
       }
   }
   ```

4. **Set up SSL (Let's Encrypt)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DATABASE_PATH=./mgnrega.db

# API Keys
DATA_API=your-data-gov-in-api-key
GEMINI_API_KEY=your-google-gemini-api-key

# Optional: Database Path
# DATABASE_PATH=/path/to/database.db
```

### Data Fetching

The application fetches data from the data.gov.in API. To update data:

```bash
# Manual data fetch
python fetch_data.py

# Or schedule with cron
# Add to crontab: 0 2 * * * /path/to/venv/bin/python /path/to/fetch_data.py
```

## API Endpoints

- `GET /` - Main dashboard
- `POST /api/geolocation` - Detect district from coordinates
- `GET /api/geolocation` - Get available districts
- `POST /api/generate-insights` - Generate AI insights

## Architecture Decisions

### Production-Ready Features

1. **Database Caching**: Local SQLite database prevents API dependency
2. **Error Handling**: Graceful degradation when APIs are unavailable
3. **Security**: Input validation, CORS protection, secure headers
4. **Performance**: Database connection pooling, query optimization
5. **Scalability**: Stateless design, easy horizontal scaling
6. **Monitoring**: Health checks, logging, error tracking

### Rural User Considerations

1. **Simple Interface**: Large buttons, clear typography, minimal clutter
2. **Local Language**: Kannada support for Karnataka users
3. **Offline Capability**: Cached data works without internet
4. **Mobile-First**: Responsive design for mobile devices
5. **Auto-Detection**: Location-based district selection

## Performance Metrics

The application tracks these MGNREGA performance indicators:

- Person-days generated (in lakhs)
- Total expenditure (in crores)
- Average days of employment
- Work completion rate (%)
- Households with 100 days work
- Female participation rate (%)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: [Your contact information]

---

**Built for India's rural citizens to make government welfare programs transparent and accessible.**
