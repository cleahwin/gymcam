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
contains_vid = False

if st.button("Provide API Key and Index ID"):
    st.subheader("API Key")
    API_KEY = st.text_input("Please provide API Key for TwelveLabs")
    st.subheader("Index ID")
    INDEX_ID = st.text_input("Please provide Index ID for TwelveLabs Index")

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
        contains_vid = gym_utils.contains_video(file_name, file_stream)
        contin = True
        if (contains_vid):
            st.warning("This video has already been added. Would you like to reclassify this video?")
            yes = st.button("Yes")
            no = st.button("No")
            if (yes and not no):
                print("hello!")
                processed_data = gym_utils.process_scores()
        else:
            # Uses visual_query function in gym_utils to retrieve scores and 
            #   collect extracted data as time segments of specific moves
            processed_data = gym_utils.process_scores()
            # Segments video input based on processed data
            # gym_utils.video_segment(processed_data)