from tkinter import Tk
from weather_app import WeatherApp
from dotenv import load_dotenv
import os

def main():
    # Load environment variables from the .env file
    load_dotenv()
    
    # Get the api key from the .env file
    api_key = os.getenv("API_KEY")
    
    if api_key is None:
        raise ValueError("API_KEY is missing. Please check the .env file.")
    
    root = Tk()  # Initialize the Tkinter window
    app = WeatherApp(root, api_key)  # Create an instance of WeatherApp
    app.run()  # Run the app

if __name__ == "__main__":
    main()