import pandas as pd
import numpy as np
import requests
import json
from io import StringIO
import time
import gym_utils

# Name of index for storing video data
INDEX_ID = "64fe445aa7e78163bd9c124a"
API_URL = "https://api.twelvelabs.io/v1.1"
TASKS_URL = f"{API_URL}/tasks"
API_KEY = "tlk_0XA82RJ21EMJBQ2THYH1P2JZMDH8"

# # default_header = {
# #     "x-api-key": API_KEY
# # }

# # INDEXES_VIDEOS_URL = f"{API_URL}/indexes/{INDEX_ID}/videos?page_limit=50"
# # response = requests.get(INDEXES_VIDEOS_URL, headers=default_header)


url = f"https://api.twelvelabs.io/v1.1/indexes/{INDEX_ID}/videos"

headers = {
    # "accept": "application/json",
    # "Content-Type": "application/json",
    "x-api-key": API_KEY
}

response = requests.get(url, headers=headers)

print(response.text)
# quit()
response_json = requests.get(
    TASKS_URL,
    headers={"x-api-key": API_KEY},
        params={"index_id": INDEX_ID, "filename": ""},
).json()
print(response_json)
for video in response_json['data']:
    print(f"VIDID ===> {video['_id']}")
    url = f"https://api.twelvelabs.io/v1.1/indexes/{INDEX_ID}/videos/{video['_id']}"
    headers2 = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    response = requests.delete(
        url, 
        headers=headers2,
        # headers={"x-api-key": API_KEY},
        params={"index_id" : INDEX_ID, "video_id" : video['_id']}
    )

    print(response.text)
# video_id_name_list = [{'video_id': video['_id'], 'video_name': video['metadata']['filename']} for video in response_json['data']]

# print(video_id_name_list)

# for elem in video_id_name_list["data"]:
#     print(elem["_id"])