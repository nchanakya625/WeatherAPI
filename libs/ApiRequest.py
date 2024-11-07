import json

import requests

#API key Fetch Code
api_key= open("API_KEY.txt", "r")

def getIP():
    response_ip = requests.get('https://httpbin.org/ip')
    ip_address = response_ip.json()['origin']
    return ip_address


def getData(args):
    host = "https://api.weatherapi.com/v1"
    path = "/current.json"
    url= f"{host}{path}?key={api_key.read()}&q={args}"
    weather_response_data = requests.get(url)
    status_code = weather_response_data.status_code
    print(f"Status Code: {status_code}")
    if status_code == 200:
        return weather_response_data.json()  # Return JSON data if successful
    elif status_code == 400:
        return {"error": "Bad Request - Invalid parameters or missing data"}
    else:
        return {"error": f"Error {status_code} - Location is incorrect or server issue"}


def extract_weather_data(data):
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
    ip= getIP()
    print(ip)
    preData = getData(ip)
    if "error" in preData:
        print(preData["error"])  # Print the error message
    else:
        for key , value in extract_weather_data(preData).items():
            print(f"{key} : {value}")


preWeatherData()
