import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from io import StringIO
import time
import gym_utils


# Name of index for storing video data
# TODO: change to empty string before uploasing
API_URL = "https://api.twelvelabs.io/v1.1"
TASKS_URL = f"{API_URL}/tasks"

st.title('GymCam')
contains_vid = False

if st.button("Provide API Key and Index ID"):
    st.subheader("API Key")
    API_KEY = st.text_input("Please provide API Key for TwelveLabs")
    INDEX_ID = gym_utils.create_index(API_KEY)

st.subheader("Upload Video")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    video_file = uploaded_file
    video_bytes = video_file.read()

    st.video(video_bytes)

    # # #### TwelveLabs Integration

    if (st.button("Save")):
        file_name = uploaded_file.name
        file_path = file_name
        file_stream = open(file_name,"rb")

        # Upload video to TwelveLab's index specified above
        contains_vid = gym_utils.upload_video(file_name, file_stream)

if (st.button("Classify")):
    file_name = uploaded_file.name
    file_path = file_name
    file_stream = open(file_name,"rb")
    processed_data = gym_utils.process_scores()
    # Uses visual_query function in gym_utils to retrieve scores and 
    #   collect extracted data as time segments of specific moves
    # Segments video input based on processed data
    # gym_utils.video_segment(processed_data)
