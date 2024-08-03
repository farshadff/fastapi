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


# @app.post("/process_audio/")
async def process_audio_file(file: UploadFile, x_user_id: str, speaker_gender: str, speaker_age: str,question: str,description: str):
    file_base64 = await read_file_as_base64(file)
    url = "https://apis.languageconfidence.ai/speech-assessment/unscripted/us"
    payload = {
        "audio_format": "mp3",
        "user_metadata": {
            "speaker_gender": speaker_gender,
            "speaker_age": speaker_age
        },
        "context": {
            "question": question,
            "context_description": description
        },
        "audio_base64": file_base64
    }
    headers = {
        "accept": "application/json",
        "x-user-id": x_user_id,
        "content-type": "application/json",
        "api-key": "sGXaUDCQjvLl48CHqykWmqIhPLmu3TiU"
    }
    # print(payload)
    # return 'done'
    response = requests.post(url, json=payload, headers=headers)
    result_data = response.json()
    # result_data = '{success:true}'
    # Store overall response
    # result_data = MOCKED_RESPONSE_DATA

    # Store overall response
    main_response = MainResponse(
        overall_score=result_data['overall'].get('overall_score'),
        mock_ielts_prediction=result_data['overall']['english_proficiency_scores']['mock_ielts'].get('prediction'),
        mock_cefr_prediction=result_data['overall']['english_proficiency_scores']['mock_cefr'].get('prediction'),
        mock_pte_prediction=result_data['overall']['english_proficiency_scores']['mock_pte'].get('prediction'),
        feedback_text=result_data.get('feedback', ''),
        overall_fluency_score=result_data['fluency'].get('overall_score'),
        overall_vocabulary_score=result_data['vocabulary'].get('overall_score'),
        overall_grammar_score=result_data['grammar'].get('overall_score'),
        overall_pronunciation_score=result_data['pronunciation'].get('overall_score'),
        tagged_transcript=result_data['fluency']['feedback'].get('tagged_transcript', ''),
        expected_text=result_data['pronunciation'].get('expected_text', ''),
        user_id=int(x_user_id),
        question=question,

    )

    async with db.begin():
        db.add(main_response)
        await db.flush()  # to get the id of the inserted row

        response_id = main_response.id

        # Store pronunciation details
        pronunciation = Pronunciation(
            response_id=response_id,
            overall_score=result_data['pronunciation'].get('overall_score'),
            lowest_scoring_phonemes=result_data['pronunciation'].get('lowest_scoring_phonemes')
        )
        db.add(pronunciation)

        # Store fluency details
        fluency = Fluency(
            response_id=response_id,
            overall_score=result_data['fluency'].get('overall_score'),
            speech_rate=result_data['fluency']['metrics'].get('speech_rate'),
            pauses=result_data['fluency']['metrics'].get('pauses'),
            filler_words=result_data['fluency']['metrics'].get('filler_words'),
            feedback_text=result_data['fluency']['feedback'].get('feedback_text', ''),
            speech_rate_over_time=result_data['fluency']['metrics'].get('speech_rate_over_time'),
            filler_words_per_min=result_data['fluency']['metrics'].get('filler_words_per_min')
        )
        db.add(fluency)

        # Store vocabulary details
        vocabulary = Vocabulary(
            response_id=response_id,
            overall_score=result_data['vocabulary'].get('overall_score'),
            vocabulary_complexity=result_data['vocabulary']['metrics'].get('vocabulary_complexity'),
            feedback_text=result_data['vocabulary']['feedback'].get('feedback_text', '')
        )
        db.add(vocabulary)

        # Store grammar details
        grammar = Grammar(
            response_id=response_id,
            overall_score=result_data['grammar'].get('overall_score'),
            feedback_text=json.dumps(result_data['grammar'].get('feedback', {}))  # Convert to JSON string
        )
        db.add(grammar)

        # Store words details
        for word in result_data['pronunciation']['words']:
            word_entry = Words(
                response_id=response_id,
                word_text=word.get('word_text'),
                word_score=word.get('word_score'),
                phoneme_data=word.get('phonemes')
            )
            db.add(word_entry)

    return {"message": "Result stored successfully"}
