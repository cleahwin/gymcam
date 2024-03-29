import pandas as pd
import numpy as np
import streamlit as st
import requests
import os
import json
from io import StringIO
import time
# import ffmpeg
from datetime import datetime
import streamlit as st

from time import sleep
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from ffmpeg import FFmpeg



INDEX_ID = ""
API_URL = "https://api.twelvelabs.io/v1.1"
TASKS_URL = f"{API_URL}/tasks"
API_KEY = ""
headers_dict = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

video_ids = []

def create_index(API_KEY):
    API_KEY = API_KEY
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
    return INDEX_ID

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
    # if (contains_video(file_name, file_stream)): 
    #     return True

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
            response = requests.post(
                TASKS_URL, 
                headers={"x-api-key": API_KEY}, 
                data=data, 
                files=file_param
            )
            # TASK_ID = response.json().get("_id")
            # TASK_ID_LIST.append(TASK_ID)
            # Check if the status code is 201 and print success
            if response.status_code == 201:
                print(f"Status code: {response.status_code} - The request was successful and a new resource was created.")
            else:
                print(f"Status code: {response.status_code}")
            print(f"File name: {file_name}")
            # print(response.json())
            print("\n")

    return False

# query_cache = {
#   "cartwheel": {<INSERT THE RESPONSE HERE that visual_query gives you when the API stops timing out>},
#   "hand stand": {<same thing here>},
# }

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
    # query_cache[pose] = result
    return response.json()

def process_scores():
    """
    Processes scores of various searches to determine the class of the move in a time segment

    Param - none
    Return - returns a list of tuples consisting of a file name, start and end time, and label name

    """
    cartwheel_results = visual_query("exercise")
    print(f"Cartwheel Results!!!! {cartwheel_results}")
    sleep(5)
    handstand_results = visual_query("handstand")
    print(f"Handstand Results!!!! {handstand_results}")

    results = []
    print("hi!")
    print(cartwheel_results)
    # for c_res in cartwheel_results["data"]:
    #     for h_res in handstand_results["data"]:
    #         if max(c_res["start"], h_res["start"]) <= min(c_res["end"], h_res["end"]):
    #             if c_res['score'] > h_res['score']:
    #                 results.append((c_res['video_id'], c_res["start"], c_res["end"], "cartwheel"))
    #             else:
    #                 results.append((h_res['video_id'], h_res["start"], h_res["end"], "handstand"))
    for c_res in cartwheel_results["data"]:
        for h_res in handstand_results["data"]:
            if max(c_res["start"], h_res["start"]) <= min(c_res["end"], h_res["end"]):
                print(f"C_RES ==> video ID {convert_video_id_to_file_name(c_res['video_id'])}, start {c_res['start']}, end {c_res['end']}")
                print(f"H_RES ==> video ID {convert_video_id_to_file_name(h_res['video_id'])}, start {h_res['start']}, end {h_res['end']}")

                if c_res['score'] > h_res['score']:
                #    sleep(5)
                   results.append((convert_video_id_to_file_name(c_res['video_id']), c_res['start'], c_res['end'], "cartwheel"))
                else:
                    # sleep(5)
                    results.append((convert_video_id_to_file_name(h_res['video_id']), h_res['start'], h_res['end'], "handstand"))
    print(f"Results ==> {results}")
    return results

def video_segment(processed_data):
    """
    Extracts video segment containing specific move and outputs to appropriate file location

    Param - list of tuples in the format (file name, start time, end time, pose)
    Return - returns the file path that the segment was saved to

    """
    for chunk in processed_data:
        print(f"CHUNK!!! ===> {chunk}")
        # now = datetime.now()
        # currTime = now.strftime("%d/%m/%Y-%H:%M:%S")
        print(f"Chunk 0 ==> {chunk[0]}")
        input_file = ffmpeg.input(chunk[0])
        output_file = ffmpeg.output(input_file, 'temp.mp4')
        ffmpeg.run(output_file)       
        # input_file = ffmpeg.input(chunk[0])
        # output_file = ffmpeg.output(
        #                 input_file.trim(start=chunk[1], end=chunk[2]), 
        #                 f"{hash(f'{chunk[3]}-{chunk[1]}-{chunk[2]}-{chunk[0]}')}.mp4"
        #             )
        # # output_file = ffmpeg.output(input_file, hash(f"{chunk[3]}-{chunk[1]}-{chunk[2]}-{chunk[0]}"), ss=chunk[1], to=chunk[2])
        # ffmpeg.run(output_file)
        # print(f"{hash(f'{chunk[3]}-{chunk[1]}-{chunk[2]}-{chunk[0]}')} + .mp4")
        # ffmpeg_extract_subclip(chunk[0], chunk[1], chunk[2], targetname=f"{hash(f'{chunk[3]}-{chunk[1]}-{chunk[2]}-{chunk[0]}')}.mp4")
        # output_file.run()
    


def convert_video_id_to_file_name(video_id):
    """
    Converts provided video id to its corresponding local file name

    Param - the video id to convert
    Return - the filename of the provided video name

    """

    url = f"https://api.twelvelabs.io/v1.1/indexes/{INDEX_ID}/videos/{video_id}"
    print(f"VIDEO_ID {video_id}")

    headers = {
        "x-api-key": API_KEY,
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    # sleep(5)
    
    return response.json().get("metadata").get("filename")


