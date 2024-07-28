from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from typing import Any
# from database import database
# from models import ServiceResult
import base64
import requests





async def read_file_as_base64(file: UploadFile) -> str:
    content = await file.read()
    return base64.b64encode(content).decode('utf-8')


async def process_audio_file(file: UploadFile):
    file_base64 = await read_file_as_base64(file)

    url = "https://apis.languageconfidence.ai/speech-assessment/unscripted/us"
    payload = {
        "audio_format": "mp3",
        "user_metadata": {
            "speaker_gender": "male",
            "speaker_age": "child"
        },
        "audio_base64": file_base64
    }
    headers = {
        "accept": "application/json",
        "x-user-id": "1",
        "content-type": "application/json",
        "api-key": "sGXaUDCQjvLl48CHqykWmqIhPLmu3TiU"
    }
    print('test')
    # response = requests.post(url, json=payload, headers=headers)
    # result_data = response.json()
    # print(result_data)
