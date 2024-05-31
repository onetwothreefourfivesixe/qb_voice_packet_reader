import pandas as pd
import threading
import time
import forced_alignment as fa
from playsound import playsound

# Function to play audio
def play_audio(file_path):
    playsound(file_path)

# Function to print text from an array at intervals
def print_text_at_intervals(text_array, intervals):
    for i in range(len(text_array)):
        print(text_array[i])
        time.sleep(intervals[i])

fa.generate_sync_map()

# File path to your audio file
audio_file = 'path_to_your_audio_file.mp3'

# Array of text to print
text_array = []

# Array of intervals (in seconds) corresponding to each text
intervals = []

# Create threads for playing audio and printing text
audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
text_thread = threading.Thread(target=print_text_at_intervals, args=(text_array, intervals))

# Start the threads
audio_thread.start()
text_thread.start()

# Wait for both threads to complete
audio_thread.join()
text_thread.join()