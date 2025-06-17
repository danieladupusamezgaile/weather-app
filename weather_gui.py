import tkinter as tk
from tkinter import messagebox
from weather_api import WeatherAPI
from PIL import Image, ImageTk # Pillow for displaying icons
import os
import json

class WeatherAppGUI:
    def __init__(self, root, api_key):
        self.api_key = api_key
        self.weather_api = WeatherAPI(api_key)
        
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
        self.root.config(bg="#628D9E")
        
        # Heading
        self.header = tk.Label(root, text="WEATHER\n FORECAST", bg="#628D9E", font=("Arial", 48))
        self.header.pack(pady=30)
        """Input field"""
        # Create Label
        self.city_label = tk.Label(root, text="Enter city:", bg="#628D9E", font=("Arial", 14))
        # Pack the label with set y padding
        self.city_label.pack(pady=5)
        # Create input field
        self.city_entry = tk.Entry(root, bg="#628D9E", font=("Arial", 14), width=25)
        # Pack the input field
        self.city_entry.pack(pady=10)
        
        # "Get Weather" button
        self.get_weather_btn = tk.Button(root, text="Get Weather", font=("Arial", 14), command=self.get_weather_from_input)
        # Pack the button
        self.get_weather_btn.pack()
        
        # Result display area
        self.result_frame = tk.Frame(root, bg="#628D9E")
        self.result_frame.pack(pady=20)
        
        # Label for weather icon
        self.weather_icon_label = tk.Label(self.result_frame, bg="#628D9E")
        self.weather_icon_label.pack()
        
        # Label wor weather info
        self.weather_label = tk.Label(self.result_frame, text="", bg="#628D9E", font=("Arial", 14))
        self.weather_label.pack()
        
        
    def get_weather_from_input(self):
        """Get the city name from the input field and display weather."""
        city_name = self.city_entry.get()
        if city_name:
            weather_data = self.weather_api.get_weather(city_name)
            self.display_weather(weather_data)
            print(json.dumps(weather_data, indent=4))
        else:
            self.display_error("Please enter a city name.")
            
    
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
            
            # Update the weather icon
            icon_code = weather['icon']
            self.update_weather_icon(icon_code)
        else:
            self.weather_label.config(text="No weather data to display.")
    
    def update_weather_icon(self, icon_code):
        # update based on weather code
        icon_path = os.path.join("weather_icons", f"{icon_code}@2x.png")
        
        if(os.path.exists(icon_path)):
            img = Image.open(icon_path)
            img = img.resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            
            self.weather_icon_label.config(image=photo)
            self.weather_icon_label.image = photo  # Keep a reference to avoid garbage collection
        else:
            print(f"Icon {icon_code} not found.")
    
    def display_error(self, error_message):
        """Display error message in a pop-up window."""
        messagebox.showerror("Error", error_message)
    
    def run(self):
        """Run the Tkinter window."""
        self.root.mainloop()