from tkinter import Tk
from weather_gui import WeatherAppGUI

def main():
    api_key = "483ed8f60b49f5c00d745614df7a0026"
    root = Tk()  # Initialize the Tkinter window
    app = WeatherAppGUI(root, api_key)  # Create an instance of WeatherApp
    app.run()  # Run the app

if __name__ == "__main__":
    main()