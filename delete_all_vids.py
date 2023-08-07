import pandas as pd
import numpy as np
import requests
import json
from io import StringIO
import time
import gym_utils

# Name of index for storing video data
INDEX_ID = "64be0834e180755b8bc4df6a"
API_URL = "https://api.twelvelabs.io/v1.1"
TASKS_URL = f"{API_URL}/tasks"
API_KEY = "tlk_0XA82RJ21EMJBQ2THYH1P2JZMDH8"

default_header = {
    "x-api-key": API_KEY
}

INDEXES_VIDEOS_URL = f"{API_URL}/indexes/{INDEX_ID}/videos?page_limit=20"
response = requests.get(INDEXES_VIDEOS_URL, headers=default_header)

response_json = response.json()
print(response_json)

for video in response_json['data']:
    print(video['_id'])
    url = "https://api.twelvelabs.io/v1.1/indexes/{INDEX_ID}/videos/{video['_id']}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    response = requests.delete(
        url, 
        headers={"x-api-key": API_KEY},
        params={"index_id" : INDEX_ID, "video_id" : video['_id']}
    )

    print(response.text)
# video_id_name_list = [{'video_id': video['_id'], 'video_name': video['metadata']['filename']} for video in response_json['data']]

# print(video_id_name_list)

# for elem in video_id_name_list["data"]:
#     print(elem["_id"])