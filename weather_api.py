import requests
import logging

# Configure logging
logging.basicConfig(filename="weather_app.log", level=logging.INFO)

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def get_weather(self, city_name):
        # Get the weather data from API for the specified city.
        url = f"{self.base_url}?q={city_name}&appid={self.api_key}&units=metric"
        
        try:
            # Set a timeout of 5 seconds for api request
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Will raise an exception for bad responses

            # Check if the status code is 200 (OK)
            if response.status_code == 200:
                logging.info(f"Successfully fetched weather data for {city_name}")
                return response.json()  # Return the JSON data
            else:
                logging.error(f"Error fetching data for {city_name}. Status code: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            logging.error("Request timed out")
            return None

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            return None