import pandas as pd
import numpy as np
import streamlit as st
import requests
import os
import json
from io import StringIO
import time
import ffmpeg
from datetime import datetime
import streamlit as st
from time import sleep



INDEX_ID = "64be0834e180755b8bc4df6a"
API_URL = "https://api.twelvelabs.io/v1.1"
TASKS_URL = f"{API_URL}/tasks"
API_KEY = "tlk_0XA82RJ21EMJBQ2THYH1P2JZMDH8"
headers_dict = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

video_ids = []

def contains_video(file_name):
    """
    Checks if index contains provided file

    Param - takes in the file name
    Return - boolean which has value true if the video was already in the index
    """

    task_list_response = requests.get(
        TASKS_URL,
        headers={"x-api-key": API_KEY},
        params={"index_id": INDEX_ID, "filename": file_name},
    )
    print(f"TaskListResponse ==> {task_list_response.json}")
    if "data" in task_list_response.json():
        task_list = task_list_response.json()["data"]
        if len(task_list) > 0:
            st.warning("This video has already been added. Please upload a new video.")
            return True
    return False


def upload_video(file_name, file_stream):
    """
    Uploads provided video file name to the GymCam index (based on index_id above)

    Param - takes in the file name and file stream
    Return - boolean which has value true if the video was already in the index
    """
<<<<<<< HEAD

    if (contains_video(file_name)): 
        return True
=======
    # if (contains_video(file_name, file_stream)): 
    #     return True
>>>>>>> 90099babcc8e1f92dfc9e44c59dbf85817fdf7d0

    # Proceed further to create a new task to index the current video if the video didn't exist in the index already
    print("Entering task creation code for the file: ", file_name)

    if file_name.endswith('.mp4'):  # Make sure the file is an MP4 video
        file_path = os.path.join('', file_name)  # Get the full path of the video file
        with open(file_path, "rb") as file_stream:
            data = {
                "index_id": INDEX_ID,
                "language": "en"
            }
            file_param = [
                ("video_file", (file_name, file_stream, "application/octet-stream")),] #The video will be indexed on the platform using the same name as the video file itself.
            response = requests.post(TASKS_URL, headers=headers_dict, data=data, files=file_param)
            TASK_ID = response.json().get("_id")
            TASK_ID_LIST.append(TASK_ID)
            # Check if the status code is 201 and print success
            if response.status_code == 201:
                print(f"Status code: {response.status_code} - The request was successful and a new resource was created.")
            else:
                print(f"Status code: {response.status_code}")
            print(f"File name: {file_name}")
            print(response.json())
            print("\n")

    return False

<<<<<<< HEAD
=======
# query_cache = {
#   "cartwheel": {<INSERT THE RESPONSE HERE that visual_query gives you when the API stops timing out>},
#   "hand stand": {<same thing here>},
# }

>>>>>>> 90099babcc8e1f92dfc9e44c59dbf85817fdf7d0
def visual_query(pose):
    """
    Performs a visual query on the video using certain searches using TwelveLabs API

    Param - pose to query on
    Return - the output of the query
    
    """
    # global query_cache
    # if pose in query_cache:
    #     return query_cache[pose]
    # Perform search with simple query (Visual)
    SEARCH_URL = f"{API_URL}/search"
    # data =  {
    #     "index_id": INDEX_ID,
    #     "search_options": ["visual"],
    #     "query": {
    #         "$not": {
    #             "origin": {
    #                 "text": "cartwheel"
    #             },
    #             "sub": {
    #                 "text": "handstand"
    #             }
    #         }
    #     }
    # }
    data = {
        "query": pose,
        "index_id": INDEX_ID,
        "search_options": ["visual"],
    }
    headers = {
        "x-api-key": API_KEY
    }
    response = requests.post(SEARCH_URL, headers=headers, json=data)
    print(response)
    print(f'Status code: {response.status_code}')
    print(f"Response from Visual Query ==> {response.json()}")
    
    result = response.json()
    # query_cache[pose] = result
    return result

def process_scores():
    """
    Processes scores of various searches to determine the class of the move in a time segment

    Param - none
    Return - returns a list of tuples consisting of a file name, start and end time, and label name

    """
    cartwheel_results = visual_query("exercise")
    # sleep(5)
    # handstand_results = visual_query("handstand")
    results = []
    print("hi!")
    print(cartwheel_results)
    for c_res in cartwheel_results["data"]:
        print("hello again!")
        for h_res in handstand_results["data"]:
            print("and again!")
            if max(c_res["start"], h_res["start"]) <= min(c_res["end"], h_res["end"]):
                if c_res['score'] > h_res['score']:
                    results.append((c_res['video_id'], c_res["start"], c_res["end"], "cartwheel"))
                else:
                    results.append((h_res['video_id'], h_res["start"], h_res["end"], "handstand"))
    # for c_res in cartwheel_results["data"]:
    #     for h_res in handstand_results["data"]:
    #         if c_res["video_id"] == h_res["video_id"] and is_overlap(c_res["start_time"], c_res["end_time"], h_res["start_time"], h_res["end_time"]):
    #             if c_res['score'] > h_res['score']:
    #                 results.append((convert_video_id_to_local_file_name(c_res['video_id']), c_res['start_time'], c_res['end_time'], "cartwheel"))
    #             else:
    #                 results.append((convert_video_id_to_local_file_name(h_res['video_id']), h_res['start_time'], h_res['end_time'], "handstand"))
    print(f"Results ==> {results}")
    return results

def video_segment(processed_data):
    """
    Extracts video segment containing specific move and outputs to appropriate file location

    Param - list of tuples in the format (file name, start time, end time, pose)
    Return - returns the file path that the segment was saved to

    """
    for chunk in processed_data:
        now = datetime.now()
        currTime = now.strftime("%d/%m/%Y-%H:%M:%S")
        
        input_file = ffmpeg.input(convert_video_id_to_file_name(chunk[0]))
        output_file = ffmpeg.output(
                        input_file.video.trim(start=chunk[1], end=chunk[2]), 
                        input_file.audio, 
                        hash(f"{chunk[3]}-{chunk[1]}-{chunk[2]}-{chunk[0]}")
                    )
        output_file.run()


def convert_video_id_to_file_name(video_id):
    """
    Converts provided video id to its corresponding local file name

    Param - the video id to convert
    Return - the filename of the provided video id

    """

    url = f"https://api.twelvelabs.io/v1.1/indexes/{INDEX_ID}/videos/{video_id}"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    return response.json().get("metadata").get("filename")


