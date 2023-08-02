import pandas as pd
import numpy as np
import requests
import json
from io import StringIO
import time
import ffmpeg
from datetime import datetime

INDEX_ID = "64be0834e180755b8bc4df6a"
API_URL = "https://api.twelvelabs.io/v1.1"
TASKS_URL = f"{API_URL}/tasks"
API_KEY = "tlk_0XA82RJ21EMJBQ2THYH1P2JZMDH8"

video_ids = []

def upload_video(file_name, file_stream):
    """
    Uploads provided video file name to the GymCam index (based on index_id above)

    Param - takes in the file name and file stream

    """

    url = "https://api.twelvelabs.io/v1.1/indexes/index-id/videos?filename=goodday"
    # TODO: Determine how to see if file name is there
    if (file_name not in requests.get(url, headers={"x-api-key": API_KEY})):
        data = {
            "index_id": INDEX_ID, 
            "language": "en"
        }
        file_param = [
            ("video_file", (file_name, file_stream, "application/octet-stream")),]
        # uploads video to index
        requests.post(TASKS_URL, headers={"x-api-key": API_KEY}, data=data, files=file_param)

        # updates list of video ids
        response = requests.get(TASKS_URL, headers={"x-api-key": API_KEY})
        video_ids.append(response.json().get('video_id'))

def visual_query():
    """
    Performs a visual query on the video using certain searches using TwelveLabs API

    Param - none
    Return - tuple containing the score of the first search and second search
    
    """
    # Perform search with simple query (Visual)
    SEARCH_URL = f"{API_URL}/search"
    data_one = {
        "query": "kick legs over",
        "index_id": INDEX_ID,
        "search_options": ["visual"],
    }
    data_two = {
        "query": "handstand",
        "index_id": INDEX_ID,
        "search_options": ["visual"],
    }
    response_one = requests.post(SEARCH_URL, headers={"x-api-key": API_KEY}, json=data_one)
    one_score = (response_one.json())['data'][0]['score']
    print (f"Status code one: {response_one.status_code}")
    print (f"One Response: {response_one.json()}")

    time.sleep(0.1)
    response_two = requests.post(SEARCH_URL, headers={"x-api-key": API_KEY}, json=data_two)
    print(f"PLAIN!: {response_two}")
    print (f"Status code handstand: {response_two.status_code}")
    print (f"Handstand Response: {response_two.json()}")

    two_score = (response_two.json())['data'][0]['score']

    return (one_score, two_score)

def process_scores():
    """
    Processes scores of various searches to determine the class of the move in a time segment

    Param - none
    Return - returns a tuple containing the move, start, and end time of it

    """

def video_segment(filename, start, end, pose):
    """
    Extracts video segment containing specific move and outputs to appropriate file location

    Param - file name of video and start time and end time of segment
    Return - returns the file path that the segment was saved to

    """
    now = datetime.now()
    currTime = now.strftime("%d/%m/%Y-%H:%M:%S")
    
    input_file = ffmpeg.input(filename)
    output_file = ffmpeg.output(
                    input_file.video.trim(start=start, end=end), 
                    input_file.audio, 
                    f"{pose}-{currTime}"
                )
    output_file.run()



