import requests
import glob
from pprint import pprint
import os

API_URL = "https://api.twelvelabs.io/v1.1"
assert API_URL

API_KEY = "tlk_0XA82RJ21EMJBQ2THYH1P2JZMDH8"
assert API_KEY

INDEXES_URL = f"{API_URL}/indexes"

INDEX_NAME = "GymCam"

headers = {
	"x-api-key": API_KEY
}

data = {
  "engine_id": "marengo2.5",
  "index_options": ["visual", "conversation", "text_in_video", "logo"],
  "index_name": INDEX_NAME,
}

response = requests.post(INDEXES_URL, headers=headers, json=data)
INDEX_ID = response.json().get('_id')
print(INDEX_ID)
print (f'Status code: {response.status_code}')
print (response.json())