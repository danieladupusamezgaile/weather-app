import tkinter as tk
from tkinter import messagebox
from weather_api import WeatherAPI
from PIL import Image, ImageTk # Pillow for displaying icons
import os

class WeatherAppGUI:
    def __init__(self, root, api_key):
        self.api_key = api_key
        self.weather_api = WeatherAPI(api_key)
        
        # Set up Tkinter window
        self.root = root
        self.root.title("Weather App")
        # Adjust window size
        self.root.geometry("300x300")
        # Set min window size
        self.root.minsize(300, 300)
        # Set max window size
        self.root.maxsize(300, 300)
        # Light blue background
        self.root.config(bg="#628D9E")
        
        # Heading
        self.header = tk.Label(root, text="WEATHER\n FORECAST", bg="#628D9E", font=("Arial", 36))
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
        self.get_weather_btn = tk.Button(root, text="Get Weather", font=("Arial", 14), command=self.open_weather_window)
        # Pack the button
        self.get_weather_btn.pack()
        
        
    def open_weather_window(self):
        city_name = self.city_entry.get()
        if city_name:
            weather_data = self.weather_api.get_weather(city_name)
            self.display_weather(weather_data)
        else:
            self.display_error("Please enter a city name.")
            
    
    def display_weather(self, data):
        # Display the weather data in new window
        if data:
            # Create a new window
            weather_window = tk.Toplevel(self.root)
            weather_window.title(f"Weather in {data['name']}")
            weather_window.config(bg="#628D9E")
            # Adjust window size
            weather_window.geometry("400x600")
            # Set min window size
            weather_window.minsize(400, 600)
            # Set max window size
            weather_window.maxsize(400, 600)
            # Light blue background
            self.root.config(bg="#628D9E")
            
            main = data['main']
            weather = data['weather'][0]
            weather_info = f"Weather in {data['name']}, {data['sys']['country']}:\n"
            weather_info += f"Temperature: {main['temp']}°C\n"
            weather_info += f"Weather: {weather['description']}\n"
            weather_info += f"Humidity: {main['humidity']}%\n"
            weather_info += f"Pressure: {main['pressure']} hPa"
            
            # Display weather icon
            icon_code = weather['icon']
            self.update_weather_icon(weather_window, icon_code)
            
            # Display weather info in the new window
            weather_label = tk.Label(weather_window, text=weather_info, bg="#628D9E", font=("Arial", 14))
            weather_label.pack(pady=10)
        else:
            self.display_error(text="No weather data to display.")
    
    def update_weather_icon(self, window, icon_code):
        # update based on weather code
        icon_path = os.path.join("weather_icons", f"{icon_code}@2x.png")
        
        if(os.path.exists(icon_path)):
            img = Image.open(icon_path)
            img = img.resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            
            # Create a label to display the icon
            weather_icon_label = tk.Label(window, image=photo, bg="#628D9E")
            weather_icon_label.pack(pady=10)
            weather_icon_label.image = photo  # Keep a reference to avoid garbage collection
        else:
            print(f"Icon {icon_code} not found.")
    
    def display_error(self, error_message):
        """Display error message in a pop-up window."""
        messagebox.showerror("Error", error_message)
    
    def run(self):
        """Run the Tkinter window."""
        self.root.mainloop()