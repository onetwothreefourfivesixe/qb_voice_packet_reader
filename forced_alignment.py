#!/usr/bin/env python
# coding=utf-8
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from aeneas.language import Language
from aeneas.syncmap import SyncMapFormat
from aeneas.task import TaskConfiguration
from aeneas.textfile import TextFileFormat
import aeneas.globalconstants as gc
import media_creator as mc
import pandas as pd

'''
Generates a synchronized map file for the provided audio and text files, based on fetched question content and reading speed.

Args:
    audio_file_path (str): The path to the audio file.
    text_file_path (str): The path to the text file.
    sync_map_file_path (str): The path to save the synchronized map file.
    question_numbers (str): Comma-separated question numbers to fetch.
    subjects (str): Comma-separated subjects to fetch questions from.
    reading_speed (float): The speed at which the text is read.

Returns:
    None
'''
def generate_sync_map(audio_file_path="audio.mp3", text_file_path="myFile.txt", sync_map_file_path="syncmap.json", question_numbers='', subjects='', reading_speed=1.0):
    try:
        # Fetch and save the audio file
        tossup, answer = mc.fetchQuestion(question_numbers, subjects)
        mc.saveSpeaking(tossup, reading_speed)
        
        # Configure task
        config = TaskConfiguration()
        config[gc.PPN_TASK_LANGUAGE] = Language.ENG
        config[gc.PPN_TASK_IS_TEXT_FILE_FORMAT] = TextFileFormat.PLAIN
        config[gc.PPN_TASK_OS_FILE_FORMAT] = SyncMapFormat.JSON
        task = Task()
        task.configuration = config
        
        # Set file paths
        task.audio_file_path_absolute = audio_file_path
        task.text_file_path_absolute = text_file_path
        task.sync_map_file_path_absolute = sync_map_file_path

        # Process task
        ExecuteTask(task).execute()

        # Print produced sync map
        task.output_sync_map_file()

        with open("answer.txt", "w", encoding="utf-8") as answerFile:
            answerFile.write(answer)
    except Exception as e:
        print(f"Error occurred: {e}")