import base64
import requests
from fastapi import UploadFile

from utils.file_utils import read_file_as_base64


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

    response = requests.post(url, json=payload, headers=headers)

    return response.json()
