import streamlit as st
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

st.title('GymCam')


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    print("Im here!")
    # # To read file as bytes:
    # bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)

    # # To convert to a string based IO:
    # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # st.write(stringio)

    # # To read file as string:
    # string_data = stringio.read()
    # st.write(string_data)

    # # Can be used wherever a "file-like" object is accepted:
    # dataframe = pd.read_csv(uploaded_file)
    # st.write(dataframe)

#     # print(f"Uploaded File {uploaded_file.name}")
    # video_file = open(uploaded_file.name, 'rb')
    video_file = uploaded_file
    video_bytes = video_file.read()

    st.video(video_bytes)

    # # #### TwelveLabs Integration
    print("Got video!")

    file_name = uploaded_file.name
    # print(f"HERE!!!!!!!!!!!!!!!!!!! {file_name}")
    file_path = file_name
    # file_path = f"C://Users//Cleah//Documents//Projects//GymCam2022//gymcam//{file_name}"
    file_stream = open(file_name,"rb")

    # Upload video to TwelveLab's index specified above
    data = {
        "index_id": INDEX_ID, 
        "language": "en"
    }
    file_param = [
        ("video_file", (file_name, file_stream, "application/octet-stream")),]
    print("Uploaded to index")
    response = requests.post(TASKS_URL, headers={"x-api-key": API_KEY}, data=data, files=file_param)
    print("Adding to index")
    response_get = requests.get(TASKS_URL, headers={"x-api-key": API_KEY})
    print(f"ResponseGet : {response_get.json().get('video_id')}")
    print("Getting index")
    
    print(response.text)

    TASK_ID = response.json().get("_id")
    print (f"Status code: {response.status_code}")
    print (response.json())

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

    print(f"One score {one_score}")

    print(f"Two score {two_score}")
    if (one_score > two_score):
        print(f"Predicting cartwheel with score {one_score}")
    else:
        print(f"Predicting handstand with score {two_score}")

# function that uploads to index