import tkinter as tk
from tkinter import messagebox
from weather_api import WeatherAPI
from PIL import Image, ImageTk # Pillow for displaying icons
import os
import math

class WeatherAppGUI:
    def __init__(self, root, api_key):
        self.api_key = api_key
        self.weather_api = WeatherAPI(api_key)
        
        # Set up Tkinter window
        self.root = root
        self.root.title("Weather App")
        # Adjust window size
        self.root.geometry("400x600")
        self.root.minsize(400, 600)
        self.root.maxsize(400, 600)
        self.root.config(bg="#628D9E")
        
        # Heading
        self.header = tk.Label(root, text="WEATHER\n FORECAST", bg="#628D9E", font=("Arial", 32))
        self.header.pack(pady=30)

        # Create Enter city Label
        self.city_label = tk.Label(root, text="Enter city:", bg="#628D9E", font=("Arial", 14))
        # Pack the label set y padding
        self.city_label.pack(pady=5)
        
        # Create city input field
        self.city_entry = tk.Entry(root, bg="#628D9E", font=("Arial", 14), width=25)
        self.city_entry.pack(pady=10)
        
        # "Get Weather" button
        self.get_weather_btn = tk.Button(root, text="Get Weather", font=("Arial", 14), command=self.button)
        self.get_weather_btn.pack()
        
        
    def button(self):
        # Save user input
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
            weather_window.minsize(400, 600)
            weather_window.maxsize(400, 600)
            self.root.config(bg="#628D9E")
            
            main = data['main']
            weather = data['weather'][0]
            
            # Display weather icon
            icon_code = weather['icon']
            self.update_weather_icon(weather_window, icon_code)
            
            # Display city
            city_label = tk.Label(weather_window, bg="#628D9E", text=f"{data['name']}, {data['sys']['country']}", font=("Arial", 22))
            city_label.pack()
            
            # Display temperature
            temp_label = tk.Label(weather_window, bg="#628D9E", text=f"{math.floor(main['temp'])}°", font=("Arial", 52))
            temp_label.pack()
            
            # Display feels like
            feels_like_label = tk.Label(weather_window, bg="#628D9E", text=f"Feels like: {math.floor(main['feels_like'])}°", font=("Arial", 14))
            feels_like_label.pack()
            
            # Display min and max temp
            min_max_temp_label = tk.Label(weather_window, bg="#628D9E", text=f"H:{math.floor(main['temp_max'])}° L:{math.floor(main['temp_min'])}°")
            min_max_temp_label.pack()
            
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