import json
import sys
from cProfile import label
from csv import excel
from http.client import responses
import logging
import requests
from logging.handlers import RotatingFileHandler
import tkinter as tk
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import Label
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os


        ############################# Logging Things in a File Initialization ################################

log_file = "../logs/app.log"
max_log_size = 5 * 1024 * 1024  # 5 MB (You can adjust this value based on your needs)
backup_count = 3  # Keep 3 backup files


logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format for the logs
    handlers=[

        RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count),  # Log to a file with rotation

    ]
)


                ################################ API key Fetch Code  ########################################
try:
    with open("../apikey/API_KEY.txt", "r") as api_key_file:
        api_key = api_key_file.read()
        logging.info("API key successfully loaded.")

except FileNotFoundError:
    print("API file not found")
    logging.error("API key file not found.")
    sys.exit()



def checkInternetConnection():
    try:
        logging.info("Checking internet connection...")
        response = requests.get("https://8.8.8.8", timeout=5)

        if response.status_code == 200 :
            logging.info("Internet connection is available.")
            return True
        else :
            logging.warning(f"Internet connection check failed with status code {response.status_code}.")
            return False
    except requests.ConnectionError as e:
        logging.error(f"Internet connection check failed: {e}")  # Log error if connection fails
        return False
def getIP():
    try:
        logging.info("Fetching IP address...")
        response_ip = requests.get('https://httpbin.org/ip')
        ip_address = response_ip.json()['origin']
        return ip_address
    except requests.RequestException as e:
        logging.error(f"Error fetching IP address: {e}")  # Log error if IP fetch fails
        return None
def getData(args):
    try :
        host = "https://api.weatherapi.com/v1"
        path = "/current.json"
        url = f"{host}{path}?key={api_key}&q={args}"
        weather_response_data = requests.get(url)
        status_code = weather_response_data.status_code
        print(f"Status Code: {status_code}")
        if status_code == 200:
            logging.info("Data successfully retrieved from API.")
            return weather_response_data.json()  # Return JSON data if successful
        elif status_code == 400:
            logging.warning("Bad Request - Invalid parameters or missing data.")
            return {"error": "Bad Request - Invalid parameters or missing data"}
        else:
            logging.error(f"Error {status_code} - Location is incorrect or server issue.")
            return {"error": f"Error {status_code} - Location is incorrect or server issue"}
    except requests.RequestException as e:
        logging.error(f"Error making API request: {e}")  # Log any exception raised during the API request
        return {"error": f"Request Exception: {e}"}
def extract_weather_data(data):
    logging.info("Extracting weather data...")  # Log data extraction
    """Extract specific weather details from the JSON response."""
    return {
        "Location Name": data['location']['name'],
        "Local Time": data['location']['localtime'],
        "Condition": data['current']['condition']['text'],
        "Condition Icon URL": data['current']['condition']['icon'],
        "Condition Code": data['current']['condition']['code'],
        "Wind Speed (kph)": data['current']['wind_kph'],
        "Humidity (%)": data['current']['humidity'],
        "Feels Like (°C)": data['current']['feelslike_c'],
        "UV Index": data['current']['uv'],
        "Temp Celsius":data['current']['temp_c']
    }
values_for_data_extraction = dict()
def preWeatherData():
    global values_for_data_extraction
    logging.info("Starting weather data retrieval process...")
    if not checkInternetConnection():
        logging.error("Internet connection is not available.")
        print("Internet Connection is not available ")
        return

    ip = getIP()
    print(ip)
    weather_fetched_data = getData(ip)
    if "error" in weather_fetched_data:
        logging.error(f"Error in getting weather data: {weather_fetched_data['error']}")
        print(weather_fetched_data["error"])  # Print the error message
    else:
        values_for_data_extraction = extract_weather_data(weather_fetched_data)
        for key, value in extract_weather_data(weather_fetched_data).items():
            print(f"{key} : {value}")
            logging.info(f"{key} : {value}")


preWeatherData()

import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import requests
from io import BytesIO


def display_image(url_or_path):
    # Check if the input is a local file path
    if os.path.isfile(url_or_path):
        # Load the image from the local file system
        image = Image.open(url_or_path)
    else:
        # Fetch image from URL
        response = requests.get(url_or_path)
        image_data = response.content
        image = Image.open(BytesIO(image_data))

    # Resize the image (if needed)
    image = image.resize((250, 250), Image.LANCZOS)

    # Convert the Image object to a format tkinter can use
    tk_image = ImageTk.PhotoImage(image)

    # Create and display the image label
    image_label = Label(window, image=tk_image)
    image_label.image = tk_image  # Store a reference to avoid garbage collection
    image_label.pack()

def button_pressed():
    print("Button pressed")




# Extracting Values for setting Images:
try :
    climate_image_url = "https:" +values_for_data_extraction["Condition Icon URL"]
except KeyError :
    climate_image_url = "../assets/error.png"



# Create tkinter window
window = tk.Tk()
window.title("Weather")
# Set the initial size of the window
window.geometry("400x600")

# Optionally, prevent resizing if you want a fixed size window
window.resizable(False, False)



# Add a label above the image
#title_label = Label(window, text="Weather API", font=("Arial", 18))
#title_label.pack(pady=10)  # Add some padding
display_image(climate_image_url)



temp_var_cel = tk.StringVar()
temp_var_fl = tk.StringVar()
condition_text = tk.StringVar()
humidity_var = tk.StringVar()
wind_speed_var = tk.StringVar()
uv_index_var = tk.StringVar()
local_date_var = tk.StringVar()
local_time_var = tk.StringVar()

try :
    temp_var_cel.set("Temperature : " + str(values_for_data_extraction["Temp Celsius"])+"°C" )
    temp_var_fl.set("Feels Like : " + str(values_for_data_extraction["Feels Like (°C)"])+"°C")
    humidity_var.set("Humidity : " + str(values_for_data_extraction["Humidity (%)"])+"%")
    wind_speed_var.set("Wind Speed : " + str(values_for_data_extraction["Wind Speed (kph)"])+" km/h")
    uv_index_var.set("UV Index : " + str(values_for_data_extraction['UV Index']))
    local_date_var.set("Date : " + str(values_for_data_extraction["Local Time"][0:10]))
    local_time_var.set("Time : " + str(values_for_data_extraction["Local Time"][10:]))
    condition_text.set(values_for_data_extraction["Condition"])
    location_name = values_for_data_extraction["Location Name"]
except KeyError:
    temp_var_cel.set("No Data Was Passed ")
    location_name = "No Internet Connection"


condition_label = Label(window, textvariable=condition_text, font=("Arial", 14))
condition_label.pack(pady = 5)

# Add another label below the image
description_label = Label(window, text=location_name, font=("Arial", 14))
description_label.pack()


temp_cel_label = tk.Label(window, textvariable=temp_var_cel, font=("Arial", 14))
temp_cel_label.pack()


temp_fl_label = tk.Label(window, textvariable=temp_var_fl, font=("Arial", 14))
temp_fl_label.pack()

humidity_label = Label(window, textvariable=humidity_var, font=("Arial", 14))
humidity_label.pack()

wind_speed_label = Label(window, textvariable=wind_speed_var, font=("Arial", 14))
wind_speed_label.pack()

uv_index_label = Label(window, textvariable=uv_index_var, font=("Arial", 14))
uv_index_label.pack()

padder_label = Label(window, text=" ", font=("Arial", 14))
padder_label.pack(pady = 5)

local_date_label = Label(window, textvariable=local_date_var, font=("Arial", 10))
local_date_label.pack()

local_time_label = Label(window, textvariable=local_time_var, font=("Arial", 10))
local_time_label.pack()

# Add a button at the bottom that prints "Button pressed" when clicked
test_button = tk.Button(window, text="Press Me", command=button_pressed, font=("Arial", 12))
test_button.pack(pady=20)


# Start the tkinter main loop
window.mainloop()

print(values_for_data_extraction["Condition"])