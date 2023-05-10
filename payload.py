
import requests
import json

payload = [
    {"name": "Contract1", "start": 0, "duration": 5, "price": 10},
    {"name": "Contract2", "start": 3, "duration": 7, "price": 14},
    {"name": "Contract3", "start": 5, "duration": 9, "price": 8},
    {"name": "Contract4", "start": 5, "duration": 9, "price": 7}
]

url = "http://localhost:8080/spaceship/optimize/"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


r = requests.post(url, data=json.dumps(payload), headers=headers)
output = r.json()

print(json.dumps(output, indent=4))
