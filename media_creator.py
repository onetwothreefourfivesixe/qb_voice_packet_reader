import pyttsx3
import json
import re
import os
import requests 

def fetchQuestion(difficulties=None, categories=None):
    url = 'https://www.qbreader.org/api/random-tossup'
    
    # Initialize params with default values
    params = {
        'difficulties': difficulties,
        'categories': categories,
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
        tossups = data['tossups'][0]['question']
        # Clean the tossups from HTML tags, parentheses, and brackets
        tossups = re.sub(r'<[^>]*>', '', tossups)
        tossups = re.sub(r'\([^)]*\)', '', tossups)
        tossups = re.sub(r'\[[^\]]*\]', '', tossups)
        return tossups
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return "An error" 

def saveSpeaking(text = ""):
    engine = pyttsx3.init()
    engine.save_to_file(text, "question.mp3")
    engine.runAndWait()
    print(text)
    with open(os.path.join('qb_packet_reader\assets',"MyFile.txt"), "w") as outputFile:
        sentences = text.split()
        for sentence in sentences:
            outputFile.write(sentence + "\n")

    return "qb_packets_reader/assets/question.mp3"

