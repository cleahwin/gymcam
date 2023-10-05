# GymCam

## Purpose
The purpose of this Streamlit app is to categorize segments of all videos in index based on whether the segment contains cartwheels or handstands.

## Approach
To do this, we used Twelve Labs search API. For each video in the index, specified by the index ID, we searched the video for cartwheels and handstands. Depending on where the searches overlapped, our algorithm writes to various files the move (cartwheel/handstand) for every time chunk. Currently, this approach results in overclassification of video chunks as cartwheels.

## File Structure
* ```gym_vid_app.py``` - streamlit app that controls all functionality of app
    * Run the app by cloning the repository and running ```streamlit run gym_vid_app.py``` in the terminal. Add videos to the repo to upload to your index.
* ```gym_utils.py``` - functions that check if video exists in index, uploads videos, queries through videos, and processes scores from videos
* ```delete_all_vids.py``` - a script that deletes all the videos in the API 
    * This file can be run by doing ```python delete_all_vids.py``` in the terminal
