# import pyttsx3
from gtts import gTTS
import json
import re
import os
import requests 

def fetchQuestion(difficulties=None, categories=None):
    url = 'https://www.qbreader.org/api/random-tossup'
    
    # Initialize params with default values
    params = {
        'difficulties': difficulties,
        'categories': ''.join([char for char in categories if char not in [';', ':', '!', '*', ' ', '[', ']','"']]),
        'number': 1,
        'minYear': 2010,
        'maxYear': 2024,
        'powermarkOnly': True,
        'standardOnly': True
    }
    
    # Make the GET request with the params dictionary
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        tossups = data['tossups'][0]['question_sanitized']
        answer = data['tossups'][0]['answer_sanitized']
        # Clean the tossups from HTML tags, parentheses, and brackets
        # tossups = re.sub(r'<[^>]*>', '', tossups)
        # tossups = re.sub(r'\([^)]\)', '', tossups)
        # tossups = re.sub(r'\[[^\]]*\]', '', tossups)
        return tossups, answer
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return "An error" 

def saveSpeaking(text = ""):
    # engine = pyttsx3.init()
    # engine.save_to_file(text, "audio.mp3")
    # engine.runAndWait()
    myobj = gTTS(text=text, lang="en", slow=False)
    myobj.save("audio.mp3")
    with open("myFile.txt", "w", encoding='utf-8') as outputFile:
        sentences = text.split()
        for sentence in sentences:
            outputFile.write(sentence + "\n")

    return "audio.mp3"

