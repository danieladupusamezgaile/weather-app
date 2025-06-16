import requests
import json

class WeatherApp:
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

    def display_weather(self, data):
        # Display the weather data
        if data:
            main = data['main']
            weather = data['weather'][0]
            print(f"Weather in {data['name']}, {data['sys']['country']}:")
            print(f"Temperature: {main['temp']}°C")
            print(f"Weather: {weather['description']}")
            print(f"Humidity: {main['humidity']}%")
            print(f"Pressure: {main['pressure']} hPa")
        else:
            print("No weather data to display.")

    def run(self):
        city_name = input("Enter the name of the city: ")
        weather_data = self.get_weather(city_name)
        self.display_weather(weather_data)


if __name__ == "__main__":
    api_key = "483ed8f60b49f5c00d745614df7a0026"
    app = WeatherApp(api_key)  # Create an instance of WeatherApp with the API key
    app.run()  # Run the app
