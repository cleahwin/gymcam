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
    video_file = uploaded_file
    video_bytes = video_file.read()

    st.video(video_bytes)

    # # #### TwelveLabs Integration
    print("Got video!")

    file_name = uploaded_file.name
    file_path = file_name
    file_stream = open(file_name,"rb")

    # Upload video to TwelveLab's index specified above
    gym_utils.upload_video(file_name, file_stream)

    # Uses visual_query function in gym_utils to retrieve scores and 
    #   collect extracted data as time segments of specific moves
    processed_data = gym_utils.process_scores()

    # Segments video input based on processed data
    gym_utils.video_segment(processed_data)