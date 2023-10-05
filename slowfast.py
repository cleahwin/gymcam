import torch
from typing import Dict
import json
import urllib
import cv2
from tqdm import tqdm        
from torchvision.transforms import Compose, Lambda
from torchvision.transforms._transforms_video import (
    CenterCropVideo,
    NormalizeVideo,
)
from pytorchvideo.data.encoded_video import EncodedVideo
from pytorchvideo.transforms import (
    ApplyTransformToKey,
    ShortSideScale,
    UniformTemporalSubsample,
    UniformCropVideo
) 

# Choose the `slowfast_r50` model 
torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
model = torch.hub.load('facebookresearch/pytorchvideo', 'slowfast_r50', pretrained=True)

# Set to GPU or CPU
device = "cpu"
model = model.eval()
model = model.to(device)

json_url = "https://dl.fbaipublicfiles.com/pyslowfast/dataset/class_names/kinetics_classnames.json"
json_filename = "kinetics_classnames.json"
try: urllib.URLopener().retrieve(json_url, json_filename)
except: urllib.request.urlretrieve(json_url, json_filename)
with open(json_filename, "r") as f:
    kinetics_classnames = json.load(f)

# Create an id to label name mapping
kinetics_id_to_classname = {}
for k, v in kinetics_classnames.items():
    kinetics_id_to_classname[v] = str(k).replace('"', "")

side_size = 256
mean = [0.45, 0.45, 0.45]
std = [0.225, 0.225, 0.225]
crop_size = 256
num_frames = 32
sampling_rate = 2
frames_per_second = 30
slowfast_alpha = 4
num_clips = 10
num_crops = 3

class PackPathway(torch.nn.Module):
    """
    Transform for converting video frames as a list of tensors. 
    """
    def __init__(self):
        super().__init__()
        
    def forward(self, frames: torch.Tensor):
        fast_pathway = frames
        # Perform temporal sampling from the fast pathway.
        slow_pathway = torch.index_select(
            frames,
            1,
            torch.linspace(
                0, frames.shape[1] - 1, frames.shape[1] // slowfast_alpha
            ).long(),
        )
        frame_list = [slow_pathway, fast_pathway]
        return frame_list

def save_chunks(cartwheel_intervals):
    print("In save_chunks!")
    # Open video
    video_path = "cartwheel.mp4"
    cap = cv2.VideoCapture(video_path)
    save_num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Read first frame
    ret, frame = cap.read()
    h, w, _ = frame.shape

    # Initialize writers to output files (1 file for each chunk)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writers = []
    num_outputs = 0
    iteration = 0
    for chunk_range in cartwheel_intervals:
        iteration = iteration + 1;
        chunk_name = f"cartwheel{iteration}.mp4"
        writers.append(cv2.VideoWriter(chunk_name, fourcc, 20.0, (w, h)))

        num_outputs += 1
        # if limit is not None and num_outputs == limit:
        #     break

    # Read and write to output files
    f = 0

        # f += 1
    for i, part in enumerate(cartwheel_intervals):
        print('hiiiiii')
        print(i)
        print(part)
        start, end = part
        while f < start:
            for j in range(frames_per_second):
                cap.read()
            f = f + 1
        while f <= end:
            for j in range(frames_per_second):
                ret, frame = cap.read()
                writers[i].write(frame)
            f = f + 1
   

    # with tqdm(total=(save_num_frames - 1)) as progress_bar:
    #     while ret:
    #         f += 1
    #         for i, part in enumerate(cartwheel_intervals):
    #             start, end = part
    #             if start <= f <= end:
    #                 # print("i has a value that is the exact same value as")
    #                 # # print(i)
    #                 for j in range(frames_per_second):
    #                     writers[i].write(frame)
    #                     ret, frame = cap.read()
    #         progress_bar.update(1)

    # for writer in writers:
    #     writer.release()

    cap.release()

def find_cartwheels(video_path):
    transform =  ApplyTransformToKey (
        key="video",
        transform=Compose(
            [
                UniformTemporalSubsample(num_frames),
                Lambda(lambda x: x/255.0),
                NormalizeVideo(mean, std),
                ShortSideScale(
                    size=side_size
                ),
                CenterCropVideo(crop_size),
                PackPathway()
            ]
        ),
    )

    # The duration of the input clip is also specific to the model.
    clip_duration = (num_frames * sampling_rate)/frames_per_second

    # Initialize an EncodedVideo helper class and load the video
    video = EncodedVideo.from_path(video_path)
    # Time length for 'chunk' that we look at a time
    chunk_secs = 2
    # List of start seconds for each 2 second chunk where there is a carthweel
    cartwheel_intervals = []
    cartwheel_combined_intervals = []
    # Whether or not the current chunk had a cartwheel in it
    has_cartwheel = False
    # Whether or not the last chunk had a cartwheel in it
    has_previous_cartwheel = False
    # Start time of the current cartwheel chunk
    current_cartwheel = 0

    chunk_frames = chunk_secs * frames_per_second
    chunk_frames_rounded = round(chunk_frames / num_frames) * num_frames
    chunk_secs = chunk_frames_rounded / frames_per_second

    print(int(video.duration))

    #TODO: Start sec starts at 2 to ignore camera setup time; change this back to 0
    #   when app has countdown for when session starts
    for start_sec in range(1, int(video.duration), int(chunk_secs) - 1):
        print(f"start_sec: {start_sec}")
        end_sec = start_sec + chunk_secs
        # Select the duration of the clip to load by specifying the start and end duration
        # The start_sec should correspond to where the action occurs in the video

        # Load the desired clip
        video_data = video.get_clip(start_sec=start_sec, end_sec=end_sec)

        # Apply a transform to normalize the video input
        video_data = transform(video_data)

        # Move the inputs to the desired device
        inputs = video_data["video"]
        inputs = [i.to(device)[None, ...] for i in inputs]

        # Pass the input clip through the model
        preds = model(inputs)

        # Get the predicted classes
        post_act = torch.nn.Softmax(dim=1)
        preds = post_act(preds)
        pred_classes = preds.topk(k=5).indices[0]

        # Map the predicted classes to the label names
        pred_class_names = [kinetics_id_to_classname[int(i)] for i in pred_classes]
        print("Top 5 predicted labels: %s" % ", ".join(pred_class_names))
        # Updates list with start time segment if chunk contained carthweel
        if "cartwheeling" in pred_class_names:
            cartwheel_intervals.append(start_sec)
            if not has_previous_cartwheel:
                current_cartwheel = start_sec
                has_previous_cartwheel = True
        else:
            if has_previous_cartwheel:
                cartwheel_combined_intervals.append((current_cartwheel, start_sec))
                has_previous_cartwheel = False
    if has_previous_cartwheel:
        cartwheel_combined_intervals.append((current_cartwheel, int(video.duration)))
        # check if time intervals containing cartwheels are consecutive

    print(cartwheel_intervals)
    
    print(f" cartwheel_combined - {cartwheel_combined_intervals}")

    return cartwheel_combined_intervals

    
video_path = 'cartwheel.mp4'
cartwheel_combined_intervals = find_cartwheels(video_path)
# find_cartwheels(video_path)
save_chunks(cartwheel_combined_intervals)