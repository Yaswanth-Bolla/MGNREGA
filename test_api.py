import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Test API call
api_key = os.getenv('DATA_API')
url = f"https://api.data.gov.in/resource/ee03643a-ee4c-48c2-ac30-9f2ff26ab722?api-key={api_key}&format=json&filters[state_name]=KARNATAKA&filters[fin_year]=2024-2025&limit=5"

print(f"Testing API with URL: {url}")

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Total records available: {data.get('total_records', 'N/A')}")
        print(f"Records returned: {len(data.get('records', []))}")

        if data.get('records'):
            print("Sample record:")
            print(data['records'][0])
        else:
            print("No records in response")
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Exception: {e}")
