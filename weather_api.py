import requests

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def get_weather(self, city_name):
        # Get the weather data from API for the specified city.
        url = f"{self.base_url}?q={city_name}&appid={self.api_key}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an exception for bad responses

            # Check if the status code is 200 (OK)
            if response.status_code == 200:
                return response.json()  # Return the JSON data
            else:
                print(f"Error: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error with the request: {e}")
            return None