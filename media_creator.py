import os
import requests 
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

'''
Fetches a random question from the QBReader API based on specified difficulties and categories.

Args:
    difficulties (list): List of difficulty levels to filter the questions.
    categories (str): String of categories to filter the questions.

Returns:
    tuple: A tuple containing the sanitized question and answer retrieved from the API.
'''
def fetchQuestion(difficulties=None, categories=None):
    url = 'https://www.qbreader.org/api/random-tossup'
    categories = ''.join(char for char in categories if char not in [';', ':', '!', '*', '[', ']', '"'])
    categories = categories.replace(', ', ',')

    # Prepare parameters
    params = {
        'difficulties': difficulties,
        'categories': categories,
        'number': 1,
        'minYear': 2010,
        'maxYear': 2024,
        'powermarkOnly': True,
        'standardOnly': True
    }

    # Make the GET request with params dictionary
    response = requests.get(url, params=params)
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        tossup = data['tossups'][0]
        return tossup['question_sanitized'], tossup['answer_sanitized']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

'''
Generates speech from the given text and saves it as an MP3 file. Also writes the text content to a UTF-8 encoded file excluding sentences with quotes.

Args:
    text (str): The text to convert to speech.
    speaking_speed (float): The speed of speech generation.

Returns:
    str: The filename of the generated audio file.
''' 
def saveSpeaking(text="", speaking_speed=1.0):
    # Synthesize speech
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

    # Write the audio content to a file
    audio_filename = "temp/audio.mp3"
    with open(audio_filename, "wb") as audio_file:
        audio_file.write(response.audio_content)
    print(f'Audio content written to file "{audio_filename}"')

    # Write sentences to a text file
    text_filename = "temp/myFile.txt"
    with open(text_filename, "w", encoding='utf-8') as output_file:
        output_file.writelines(sentence + "\n"for sentence in text.split()) #if'("'not in sentence

    return audio_filename