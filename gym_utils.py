import pandas as pd
import numpy as np
import streamlit as st
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
    print(requests.get(url, headers={"x-api-key": API_KEY}).json())
    # TODO: Determine how to see if file name is there
    if (file_name in requests.get(url, headers={"x-api-key": API_KEY})):
        # Handles case that video has already been added
        st.warning("This video has already been added. Please upload a new video.")
    else:
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

def visual_query(pose):
    """
    Performs a visual query on the video using certain searches using TwelveLabs API

    Param - pose to query on
    Return - map of 
    
    """
    # Perform search with simple query (Visual)
    SEARCH_URL = f"{API_URL}/search"
    data = {
        "query": pose,
        "index_id": INDEX_ID,
        "search_options": ["visual"],
    }
    response_one = requests.post(SEARCH_URL, headers={"x-api-key": API_KEY}, json=data)
    one_score = (response_one.json())['data'][0]['score']
    print (f"Status code one: {response_one.status_code}")
    print (f"One Response: {response_one.json()}")

    return (one_score, two_score)

def process_scores():
    """
    Processes scores of various searches to determine the class of the move in a time segment

    Param - none
    Return - returns a list of tuples consisting of a file name, start and end time, and label name

    """
    # cartwheel_results = visual_query("cartwheel")
    # handstand_results = visual_query("handstand")
    # results = []
    # for c_res in cartwheel_results:
    #     for h_res in handstand_results:
    #         if is_overlap(c_res["start_time"], c_res["end_time"], h_res["start_time"], h_res["end_time"]):
    #             if c_res['score'] > h_res['score']:
    #                 results.append((convert_video_id_to_local_file_name(c_res['video_id']), c_res['start_time'], c_res['end_time'], "cartwheel")
    #             else:
    #                 results.append((convert_video_id_to_local_file_name(h_res['video_id']), h_res['start_time'], h_res['end_time'], "handstand")
    # return results

def video_segment(processed_data):
    """
    Extracts video segment containing specific move and outputs to appropriate file location

    Param - list of tuples in the format (file name, start time, end time, pose)
    Return - returns the file path that the segment was saved to

    """
    for chunk in processed_data:
        now = datetime.now()
        currTime = now.strftime("%d/%m/%Y-%H:%M:%S")
        
        input_file = ffmpeg.input(chunk[0])
        output_file = ffmpeg.output(
                        input_file.video.trim(start=chunk[1], end=chunk[2]), 
                        input_file.audio, 
                        f"{chunk[3]}-{currTime}"
                    )
        output_file.run()



