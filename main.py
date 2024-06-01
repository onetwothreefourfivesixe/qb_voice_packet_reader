import pandas as pd
import json
import threading
import time
import forced_alignment as fa
from pygame import mixer

# Read from syncmap json
def read_from_sync_json(readData = "begin", filePath = "syncmap.json"):
    data = json.load(open(filePath))
    arrayOfData = []
    for fragment in data["fragments"]:
        if readData == "begin":
            arrayOfData.append(float(fragment["end"]) - float(fragment["begin"]))
        else:
            arrayOfData.append(fragment[readData])
    return arrayOfData

# Function to play audio
def play_audio(file_path):
    mixer.init()
    mixer.music.load(file_path)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)
    mixer.music.stop()

# Function to print text from an array at intervals
def print_text_at_intervals(text_array, intervals):
    for i in range(len(text_array)):
        print(text_array[i])
        time.sleep(intervals[i])

fa.generate_sync_map()

# File path to your audio file
audio_file = "audio.mp3"



# Array of text to print
text_array = read_from_sync_json("lines")

# Array of intervals (in seconds) corresponding to each text
intervals = read_from_sync_json()

# Create threads for playing audio and printing text
audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
text_thread = threading.Thread(target=print_text_at_intervals, args=(text_array, intervals))

# Start the threads
audio_thread.start()
text_thread.start()

# Wait for both threads to complete
audio_thread.join()
text_thread.join()