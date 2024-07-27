from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from typing import Any
from database import database
from models import ServiceResult
import base64
import requests

app = FastAPI()


class ServiceResultCreate(BaseModel):
    user: str
    type: str
    result: Any
    date_fa: str


async def read_file_as_base64(file: UploadFile) -> str:
    content = await file.read()
    return base64.b64encode(content).decode('utf-8')


@app.post("/process_audio/")
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
    result_data = response.json()
    print(result_data)
    service_result = ServiceResult(
        user="1",  # Update with actual user id if available
        type="audio_assessment",
        result=result_data,
        date_fa="current_date_in_fa_format"  # Replace with actual date in Farsi format if required
    )

    query = ServiceResult.__table__.insert().values(
        user=service_result.user,
        type=service_result.type,
        result=service_result.result,
        date=service_result.date,
        date_fa=service_result.date_fa
    )

    await database.execute(query)

    return {"message": "Result stored successfully"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
