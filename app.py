from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os
from flask_caching import Cache

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})

app.config['TOMORROW_API_KEY'] = os.getenv('TOMORROW_API_KEY')
app.config['LOCATION_API_URL'] = 'https://ipapi.co/{ip}/json/'
app.config['WEATHER_API_URL'] = 'https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={api_key}'

@cache.memoize(timeout=3600)
def get_location_by_ip(ip_address):
    try:
        url = app.config['LOCATION_API_URL'].format(ip=ip_address)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        city = data.get('city')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not city or not latitude or not longitude:
            return {"error": "Location data is incomplete"}, None, None, None

        return city, latitude, longitude

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving location data: {e}")
        return {"error": f"Failed to retrieve location data: {e}"}, None, None

@cache.memoize(timeout=600)
def get_weather(latitude, longitude):
    url = app.config['WEATHER_API_URL'].format(lat=latitude, lon=longitude, api_key=app.config['TOMORROW_API_KEY'])
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        temperature = data['data']['values'].get('temperature')
        
        if temperature is None:
            return {"error": "Weather data is incomplete"}
        
        return temperature

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving weather data: {e}")
        return {"error": f"Failed to retrieve weather data: {e}"}

@app.route('/', methods=['GET'])
def weather():
    user_ip = request.remote_addr
    location_data, latitude, longitude = get_location_by_ip(user_ip)

    if isinstance(location_data, dict) and "error" in location_data:
        return jsonify(location_data), 500

    temperature = get_weather(latitude, longitude)
    if isinstance(temperature, dict) and "error" in temperature:
        return jsonify(temperature), 500

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({
        "city": location_data,
        "weather": f"{temperature}°C",
        "time": current_time
    })

if __name__ == '__main__':
    app.run(debug=True)