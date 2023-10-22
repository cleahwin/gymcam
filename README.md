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

## How to Use the Web App
Upon opening the app, the folowing page will open. 
![Screenshot of home page of web app. "GymCam" is written in large text at the top. Below, is a button that says "Provide API Key and Index ID". Below, is "Upload Video" written as a second heading level. Below is "Choose a file" and a interface for uploading files with a button "Browse files". At the bottom is a button that says "Classify".](docs/images/first-screenshot.png)


First, an API key to the TwelveLabs account should be provided by clicking on the "Provide API Key and Index ID" button, entering the key, and then pressing "Done", as shown in the screenshot below. The API key can be found after creating an account on TwelveLabs.
![Screenshot of same page as in the previous image after pressing "Provide  API Key and Index ID". Now, in addition to the content before, there is now "API Key" written in heading level 2 text, the text "Please proivde API Key for TwelveLabs", an entry text box, and a "Done button", immeidately below the "Provide  API Key and Index ID".](docs/images/screenshot-clicked-api-key.png)

Then, videos can be uploaded from one's local computer by clicking on Browse Files, Save, and Classify as shown in the image below. 
![Screenshot of same page as in the previous images after pressing "Browse Files" button. Now, in addition to the content before, there is a preview of a video with two people doing archery below the "browse files" button. Below this video are two buttons that say "Save" and "Classify".](docs/images/screnshot_upload_video.png)

