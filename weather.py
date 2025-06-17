import requests
import json
import tkinter as tk
from tkinter import messagebox

class WeatherApp:
    def __init__(self, api_key, root):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Set up Tkinter window
        self.root = root
        self.root.title("Weather App")
        # Adjust window size
        self.root.geometry("400x600")
        # Set min window size
        self.root.minsize(400, 600)
        # Set max window size
        self.root.maxsize(400, 600)
        # Light blue background
        self.root.config(bg="#AEE0F5")
        
        """Input field"""
        # Create Label
        self.city_label = tk.Label(root, text="Enter the name of the city", bg="#AEE0F5", font=("Arial", 14))
        # Pack the label with set y padding
        self.city_label.pack(pady=10)
        # Create input field
        self.city_entry = tk.Entry(root, bg="#AEE0F5", font=("Arial", 14), width=25)
        # Pack the input field
        self.city_entry.pack(pady=10)
        
        # "Get Weather" button
        self.get_weather_btn = tk.Button(root, text="Get Weather", font=("Arial", 14), command=self.get_weather_from_input)
        # Pack the button
        self.get_weather_btn.pack(pady=10)
        
        # Result display area
        self.result_frame = tk.Frame(root, bg="#AEE0F5")
        self.result_frame.pack(pady=20)
        
        self.weather_label = tk.Label(self.result_frame, text="", bg="#AEE0F5", font=("Arial", 14))
        self.weather_label.pack()
        

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
            weather_info = f"Weather in {data['name']}, {data['sys']['country']}:\n"
            weather_info += f"Temperature: {main['temp']}°C\n"
            weather_info += f"Weather: {weather['description']}\n"
            weather_info += f"Humidity: {main['humidity']}%\n"
            weather_info += f"Pressure: {main['pressure']} hPa"
            
            self.weather_label.config(text=weather_info)
        else:
            self.weather_label.config(text="No weather data to display.")

    def display_error(self, error_message):
        """Display error message in a pop-up window."""
        messagebox.showerror("Error", error_message)

    def get_weather_from_input(self):
        """Get the city name from the input field and display weather."""
        city_name = self.city_entry.get()
        if city_name:
            weather_data = self.get_weather(city_name)
            self.display_weather(weather_data)
        else:
            self.display_error("Please enter a city name.")

    def run(self):
        """Run the Tkinter window."""
        self.root.mainloop()



if __name__ == "__main__":
    api_key = "483ed8f60b49f5c00d745614df7a0026"
    root = tk.Tk()  # Initialize the Tkinter window
    app = WeatherApp(api_key, root)  # Create an instance of WeatherApp
    app.run()  # Run the app
    