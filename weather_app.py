import tkinter as tk
from weather_api import WeatherAPI
from tkinter import messagebox, ttk
import logging
import math
from PIL import Image, ImageTk  # Pillow for displaying icons
import os
import threading

# Configure the logger
logging.basicConfig(filename='weather_app.log', level=logging.INFO)

# Constants for colors and fonts
BG_COLOR = "#628D9E"
FONT_LARGE = ("Arial", 52)
FONT_MEDIUM = ("Arial", 22)
FONT_SMALL = ("Arial", 14)

class WeatherApp:
    def __init__(self, root, api_key):
        self.api_key = api_key
        self.weather_api = WeatherAPI(api_key)
        self.root = root
        # set up home window
        self._setup_window(self.root, "Weather App", 400, 600)
        
        # Create frames for each screen
        self.city_input_frame = self._create_city_input_frame()
        self.weather_info_frame = self._create_weather_info_frame()
        
        # Loading indicator
        self.loading_indicator = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="indeterminate")
        
        # Initially, display the city input screen
        self.city_input_frame.pack(fill="both", expand=True)
    
    def _setup_window(self, window, title, width, height):
        # Set up the window size and title.
        window.title(title)
        window.geometry(f"{width}x{height}")
        window.minsize(width, height)
        window.maxsize(width, height)
        window.config(bg=BG_COLOR)
    
    def _create_city_input_frame(self):
        # create frame for city input screen
        frame = tk.Frame(self.root, bg=BG_COLOR)
        
        # Heading
        self.heading = self._create_label(frame, "WEATHER\n FORECAST", FONT_LARGE, 30)
        # City input
        self.city_label = self._create_label(frame, "Enter city:", FONT_SMALL, 5)
        self.city_entry = self._create_entry(frame, FONT_SMALL, 25, 10)
        # "Select" button
        self.select_btn = self._create_button(frame, "Select", self.fetch_weather)

        return frame
    
    def _create_weather_info_frame(self):
        # create frame for weather info screen
        frame = tk.Frame(self.root, bg=BG_COLOR)
        
        # Display 'back' button
        self.back_btn = self._create_button(frame, "←", self.show_city_input_screen)
        self.back_btn.place(x=10, y=10)
        # Weather icon label
        self.weather_icon_label = tk.Label(frame, bg=BG_COLOR)
        self.weather_icon_label.pack(pady=10)
        # Display weather info
        self.city_info = self._create_label(frame, "", FONT_MEDIUM)
        self.temp_info = self._create_label(frame, "", FONT_LARGE)
        self.feels_like_info = self._create_label(frame, "", FONT_SMALL)
        self.max_min_temp_info = self._create_label(frame, "", FONT_SMALL) 
        
        return frame

    def _create_label(self, window, text, font, pady=None):
        label = tk.Label(window, text=text, bg=BG_COLOR, font=font)
        label.pack(pady=pady)
        return label
    
    def _create_entry(self, window, font, width, pady):
        entry = tk.Entry(window, bg=BG_COLOR, font=font, width=width)
        entry.pack(pady=pady)
        return entry
    
    def _create_button(self, window, text, command, justify="center"):
        button = tk.Button(window, text=text, font=FONT_SMALL, justify=justify, command=command)
        button.pack()
        return button
    
    def fetch_weather(self):
        # Save user input
        city_name = self.city_entry.get()
        if city_name:
            # Show the loading indicator
            self.loading_indicator.pack(pady=10)
            self.loading_indicator.start()  # Start the loading animation
            
            # Run fetch_weather_in_thread function in a separate thread
            threading.Thread(target=self.fetch_weather_in_thread, args=(city_name,)).start()
        else:
            self.display_error("Please enter a city name.")
            
    def fetch_weather_in_thread(self, city_name):
        try:
            weather_data = self.weather_api.get_weather(city_name)
            self.display_weather(weather_data)
        except Exception as e:
            self.display_error(f"Error fetching weather data: {e}")
        finally:
            # Stop the loading indicator after the data is fetched
            self.loading_indicator.stop()
            self.loading_indicator.pack_forget()

    def display_weather(self, data):
        # Display the weather data
        if data:
            main = data['main']
            weather = data['weather'][0]
            icon_code = weather['icon']
            
            # Hide the city input screen and show the weather display
            self.city_input_frame.pack_forget()
            
            # Display weather icon
            self.update_weather_icon(icon_code)
            
            # Update weather info
            self.city_info.config(text=f"{data['name']}, {data['sys']['country']}")
            self.temp_info.config(text=f"{math.floor(main['temp'])}°")
            self.feels_like_info.config(text=f"Feels like: {math.floor(main['feels_like'])}°")
            self.max_min_temp_info.config(text=f"H:{math.floor(main['temp_max'])}° L:{math.floor(main['temp_min'])}°")
            
            # Show weather info screen
            self.weather_info_frame.pack(fill="both", expand=True)
        else:
            self.display_error(text="No weather data to display.")
    
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
            self.display_error(f"Icon {icon_code} not found.")
    
    def show_city_input_screen(self):
        # Switch back to the city input screen.
        self.weather_info_frame.pack_forget()
        self.city_input_frame.pack(fill="both", expand=True)
    
    def display_error(self, error_message):
        """Display error message in a pop-up window."""
        logging.error(f"Error: {error_message}")
        messagebox.showerror("Error", error_message)
    
    def run(self):
        """Run the Tkinter window."""
        self.root.mainloop()
