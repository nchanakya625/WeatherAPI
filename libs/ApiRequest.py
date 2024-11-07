import json
import sys
from http.client import responses
import logging
import requests
from logging.handlers import RotatingFileHandler


        ############################# Logging Things in a File Initialization ################################

log_file = "app.log"
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
    with open("API_KEY.txt", "r") as api_key_file:
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
        "UV Index": data['current']['uv']
    }


def preWeatherData():
    logging.info("Starting weather data retrieval process...")
    if not checkInternetConnection():
        logging.error("Internet connection is not available.")
        print("Internet Connection is not available ")
        return

    ip = getIP()
    print(ip)
    preData = getData(ip)
    if "error" in preData:
        logging.error(f"Error in getting weather data: {preData['error']}")
        print(preData["error"])  # Print the error message
    else:
        for key, value in extract_weather_data(preData).items():
            print(f"{key} : {value}")
            logging.info(f"{key} : {value}")


preWeatherData()
