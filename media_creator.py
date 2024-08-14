# import pyttsx3
from gtts import gTTS
import json
import re
import os
import requests 
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

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

def saveSpeaking(text = "", speaking_speed=1.0):
    # engine = pyttsx3.init()
    # engine.save_to_file(text, "audio.mp3")
    # engine.runAndWait()
    # myobj = gTTS(text=text, lang="en", slow=False)
    # myobj.save("audio.mp3")
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speaking_speed
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open("audio.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    with open("myFile.txt", "w", encoding='utf-8') as outputFile:
        sentences = text.split()
        for sentence in sentences:
            if not '("' in sentence:
                outputFile.write(sentence + "\n")

    return "audio.mp3"

