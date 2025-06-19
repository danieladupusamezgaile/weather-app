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
            logging.info(f"Sending request to fetch weather data for {city_name}")
            # Set a timeout of 5 seconds for api request
            response = requests.get(url, timeout=5)
            # response.raise_for_status()  # Will raise an exception for bad responses
            logging.info(f"Response recieved for {city_name}")
            # Check if the status code is 404 (City Not Found)
            if response.status_code == 404:
                raise Exception(f"City '{city_name}' not found. Please check the city name.")
            # Check if the status code is 200 (OK)
            elif response.status_code == 200:
                return response.json()  # Return the JSON data
            else:
                raise Exception(f"Failed to get weather for {city_name}")

        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out for: {city_name}", )

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error for {city_name}")

        except Exception as e:
            raise Exception(f"An error occured: {str(e)}")
