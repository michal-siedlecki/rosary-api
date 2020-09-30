import requests
import json


BASE_URL = "http://127.0.0.1:5000/api/1"
ENDPOINT = ""
URL = BASE_URL + ENDPOINT

data = json.dumps({
    "parts": ["radosne", "bolesne", "chwalebne"],
    "duration": 30
})

requests.post(url=URL, data=data)


