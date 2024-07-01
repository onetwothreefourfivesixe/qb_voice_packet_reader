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

def generate_sync_map(audio_file_path = "audio.mp3", text_file_path = "myFile.txt", sync_map_file_path = "syncmap.json", question_numbers='1, 2, 3, 4, 5, 6, 7, 8, 9, 10', subjects='History, Science, Literature, Fine Arts'):
    # Fetch and save the audio file
    tossup, answer = mc.fetchQuestion(question_numbers, subjects)
    mc.saveSpeaking(tossup)
    
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

    with open("answer.txt", "w") as answerFile:
        answerFile.write(answer)