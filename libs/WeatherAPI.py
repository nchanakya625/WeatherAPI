import requests

# Define the URL
url = "https://api.example.com/data"

# Send a GET request
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response data as JSON (if the API returns JSON)
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
import http.client
import json

# Define the URL components
host = "api.example.com"
path = "/data"

# Create a connection
conn = http.client.HTTPSConnection(host)

# Send a GET request
conn.request("GET", path)

# Get the response
response = conn.getresponse()

# Check if the request was successful (status code 200)
if response.status == 200:
    # Parse the response data as JSON
    data = json.loads(response.read().decode())
    print(data)
else:
    print(f"Error: {response.status}")

# Close the connection
conn.close()