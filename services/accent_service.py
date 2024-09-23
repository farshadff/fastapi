import json
from fastapi import Request, UploadFile, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
# from models import MainResponse, PronunciationResponse, WordDetails
import base64
from database import database as db
import requests

router = APIRouter()


async def read_file_as_base64(file: UploadFile) -> str:
    content = await file.read()
    return base64.b64encode(content).decode('utf-8')


# @app.post("/accent-service/")
async def process_accent_file(
        file: UploadFile,
        x_user_id: str,
        speaker_gender: str,
        speaker_age: str,
        question: str,
        description: str,
        expected_text: str,
        db: AsyncSession
):
    file_base64 = await read_file_as_base64(file)

    # Call the new pronunciation service
    url = "https://apis.languageconfidence.ai/pronunciation/us"
    payload = {
        "audio_format": "wav",
        "expected_text": expected_text,
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

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error calling pronunciation service")

    result_data = response.json()

    # Store the response in the database
    # pronunciation_response_id = await store_pronunciation_response(result_data, db)

    return {"message": "Result stored successfully", "response_datax": result_data,
            "pronunciation_response_id": 1}


# async def store_pronunciation_response(result_data: dict, db: AsyncSession) -> int:
#     """Store pronunciation response and related word details in the database."""
#
#     pronunciation_response = PronunciationResponse(
#         overall_score=result_data.get("overall_score", 0.0),
#         expected_text=result_data.get("expected_text", ""),
#         mock_ielts_prediction=result_data.get("english_proficiency_scores", {}).get("mock_ielts", {}).get("prediction",
#                                                                                                           None),
#         mock_cefr_prediction=result_data.get("english_proficiency_scores", {}).get("mock_cefr", {}).get("prediction",
#                                                                                                         None),
#         mock_pte_prediction=result_data.get("english_proficiency_scores", {}).get("mock_pte", {}).get("prediction",
#                                                                                                       None),
#         lowest_scoring_phonemes=result_data.get("lowest_scoring_phonemes", []),
#         warnings=result_data.get("warnings", {})
#     )
#
#     async with db.begin():
#         db.add(pronunciation_response)
#         await db.flush()  # to get the id of the inserted row
#
#         # Store word details
#         for word_data in result_data.get("words", []):
#             word_details = WordDetails(
#                 word_text=word_data.get("word_text", ""),
#                 word_score=word_data.get("word_score", 0.0),
#                 phonemes=word_data.get("phonemes", []),
#                 pronunciation_response_id=pronunciation_response.id
#             )
#             db.add(word_details)
#
#     return pronunciation_response.id
