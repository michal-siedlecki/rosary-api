import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/1"
ENDPOINT = "/1"

URL = BASE_URL + ENDPOINT

data = json.dumps(
    {
        "reserved": True,
    }
)

requests.put(url=URL, data=data)
