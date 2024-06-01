import pygame
import threading
import time
import json
import forced_alignment

# Initialize pygame mixer
pygame.mixer.init()
forced_alignment.generate_sync_map()

# Read from syncmap json
def read_from_sync_json(readData="begin", filePath="syncmap.json"):
    with open(filePath, 'r') as file:
        data = json.load(file)
    arrayOfData = []
    for fragment in data["fragments"]:
        if readData == "begin":
            arrayOfData.append(float(fragment["end"]) - float(fragment["begin"]))
        else:
            arrayOfData.append(fragment[readData])
    return arrayOfData

# Function to play audio
def play_audio(file_path, pause_event, resume_event):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if pause_event.is_set():
            pygame.mixer.music.pause()
            resume_event.wait()  # Wait until resume_event is set
            pygame.mixer.music.unpause()
        time.sleep(0.1)
    pygame.mixer.music.stop()

# Function to print text from an array at intervals
def print_text_at_intervals(text_array, intervals, pause_event, resume_event):
    for i in range(len(text_array)):
        print(text_array[i])
        time.sleep(intervals[i])
        while pause_event.is_set():
            resume_event.wait()  # Wait until resume_event is set

# Setup pygame window
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Audio and Text Synchronization")

# Event objects to control pausing and resuming
pause_event = threading.Event()
resume_event = threading.Event()

# File path to your audio file
audio_file = "audio.mp3"

# Array of text to print
text_array = read_from_sync_json("lines")

# Array of intervals (in seconds) corresponding to each text
intervals = read_from_sync_json()

# Create threads for playing audio and printing text
audio_thread = threading.Thread(target=play_audio, args=(audio_file, pause_event, resume_event))
text_thread = threading.Thread(target=print_text_at_intervals, args=(text_array, intervals, pause_event, resume_event))

# Start the threads
audio_thread.start()
text_thread.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.mixer.music.stop()
            pause_event.set()  # Pause the threads
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not pause_event.is_set():
                    print("Pausing...")
                    pause_event.set()  # Pause both threads
                else:
                    print("Resuming...")
                    resume_event.set()  # Resume both threads
                    pause_event.clear()
                    resume_event.clear()
    
    # Fill the screen with white
    screen.fill((255, 255, 255))
    
    # Update the display
    pygame.display.flip()

# Wait for both threads to complete
audio_thread.join()
text_thread.join()

pygame.quit()
