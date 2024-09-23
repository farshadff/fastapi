import json
from fastapi import Request
import requests
from fastapi import UploadFile, APIRouter
from pydantic import BaseModel
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from models import MainResponse, Pronunciation, Fluency, Vocabulary, Grammar, Words
import base64
from database import database as db

router = APIRouter()


class ServiceResultCreate(BaseModel):
    user: str
    type: str
    result: Any
    date_fa: str


async def read_file_as_base64(file: UploadFile) -> str:
    content = await file.read()
    return base64.b64encode(content).decode('utf-8')


# @app.post("/accent-service/")
async def process_accent_file(file: UploadFile, x_user_id: str, speaker_gender: str, speaker_age: str, question: str,
                             description: str, db: AsyncSession):
    file_base64 = await read_file_as_base64(file)
    """Call the new pronunciation service."""
    url = "https://apis.languageconfidence.ai/pronunciation/us"
    payload = {
        "audio_format": "wav",
        "expected_text": "test",
        "user_metadata": {
            "speaker_gender": speaker_gender,
            "speaker_age": speaker_age
        },
        "audio_base64": file_base64
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": "sGXaUDCQjvLl48CHqykWmqIhPLmu3TiU"
    }

    # return x_user_id
    # Send request to the external API
    response = requests.post(url, json=payload, headers=headers)
    result_data = response.json()
    print(result_data)
    # Handle base64 processing error

    return {"message": "Result stored successfully", "response_datax": result_data}
