
# Weather Forecast API

This Flask API provides weather forecast information based on a user's IP address using Flask, caching, and the Tomorrow.io API.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Application](#running-the-application)
5. [Code Structure](#code-structure)
6. [Usage](#usage)
7. [License](#license)

## Features

- Retrieves location based on IP address
- Fetches current weather data using Tomorrow.io API
- Caches location and weather data for a defined duration to improve performance

## Prerequisites

- Python 3.x
- Valid API Key for Tomorrow.io (for weather data fetching)
- Required Python packages listed in the `requirements.txt` file

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/razmazlih/MyWeather.git
   cd MyWeather
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root directory.
   - Add your Tomorrow.io API key:
     ```
     TOMORROW_API_KEY=your_api_key_here
     ```

## Running the Application

Start the Flask app using:
```bash
flask run
```

By default, it runs on `http://127.0.0.1:5000/`.

## Code Structure

- `app.py`: The main application file containing the routes and logic.
- `get_location_by_ip()`: Fetches location details based on IP using `ipapi`.
- `get_weather()`: Retrieves real-time weather data for a given latitude and longitude.
- `cache`: Caches results for faster response times.

## Usage

After starting the server, send a GET request to the root endpoint:
```
http://127.0.0.1:5000/
```

The response contains:
- `city`: The detected city based on the IP address.
- `weather`: Current temperature in Celsius.
- `time`: Current server time.

## License

This project is licensed under the MIT License.
