from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

TOMORROW_API_KEY = os.getenv('TOMORROW_API_KEY')

def get_location_by_ip(ip_address):
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        response.raise_for_status()
        data = response.json()
        city = data.get('city')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        return city, latitude, longitude
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving location data: {e}")
        return None, None, None

def get_weather(latitude, longitude):
    url = f'https://api.tomorrow.io/v4/weather/realtime?location={latitude},{longitude}&apikey={TOMORROW_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temperature = data['data']['values'].get('temperature')
        return temperature
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving weather data: {e}")
        return None

@app.route('/', methods=['GET'])
def weather():
    user_ip = request.remote_addr

    city, latitude, longitude = get_location_by_ip(user_ip)

    if city and latitude and longitude:
        temperature = get_weather(latitude, longitude)
        
        if temperature is not None:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify({
                "city": city,
                "weather": f"{temperature}°C",
                "time": current_time
            })
        else:
            return jsonify({"error": "Failed to retrieve weather data"}), 500
    else:
        return jsonify({"error": "Failed to retrieve location data"}), 500

if __name__ == '__main__':
    app.run(debug=True)