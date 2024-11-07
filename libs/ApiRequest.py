import http.client as requests
import json


host = "api.example.com"
path = "/data"

conn = http.client.HTTPSConnection(host)

conn.request("GET", path)

response = conn.getresponse()

if response.status == 200:
    data = json.loads(response.read().decode())
    print(data)
else:
    print(f"Error: {response.status}")
conn.close()