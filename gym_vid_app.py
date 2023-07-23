import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import StringIO

# Name of index for storing video data
INDEX_ID = "GymCam"
API_URL = "https://api.twelvelabs.io/v1.1"
TASKS_URL = f"{API_URL}/tasks"
API_KEY = "tlk_0XA82RJ21EMJBQ2THYH1P2JZMDH8"

st.title('GymCam')


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

    # print(f"Uploaded File {uploaded_file.name}")
    video_file = open(uploaded_file.name, 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)

# #### TwelveLabs Integration


file_name = "cartwheel_short_one.mp4"
file_path = "C://Users//Cleah//Documents//Projects//GymCam2022//gymcam//cartwheel_short_one.mp4"
file_stream = open(file_path,"rb")

data = {
    "index_id": INDEX_ID, 
    "language": "en"
}
file_param = [
    ("video_file", (file_name, file_stream, "application/octet-stream")),]

response = requests.post(TASKS_URL, headers={"x-api-key": API_KEY}, data=data, files=file_param)

TASK_ID = response.json().get("_id")
print (f"Status code: {response.status_code}")
print (response.json())