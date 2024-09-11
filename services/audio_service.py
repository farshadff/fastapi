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
async def process_audio_file(file: UploadFile, x_user_id: str, speaker_gender: str, speaker_age: str, question: str,
                             description: str, db: AsyncSession):
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

    # Send request to the external API
    response = requests.post(url, json=payload, headers=headers)
    result_data = response.json()
    print(result_data)
    # Handle base64 processing error
    if 'detail' in result_data and result_data['detail'] == 'Unable to process the base64 audio':
        return {"error": result_data['detail']}

    # Store overall response
    main_response = MainResponse(
        overall_score=result_data.get('overall', {}).get('overall_score', None),
        mock_ielts_prediction=result_data.get('overall', {}).get('english_proficiency_scores', {}).get('mock_ielts',
                                                                                                       {}).get(
            'prediction', None),
        mock_cefr_prediction=result_data.get('overall', {}).get('english_proficiency_scores', {}).get('mock_cefr',
                                                                                                      {}).get(
            'prediction', None),
        mock_pte_prediction=result_data.get('overall', {}).get('english_proficiency_scores', {}).get('mock_pte',
                                                                                                     {}).get(
            'prediction', None),
        feedback_text=result_data.get('feedback', ''),
        overall_fluency_score=result_data.get('fluency', {}).get('overall_score', None),
        overall_vocabulary_score=result_data.get('vocabulary', {}).get('overall_score', None),
        overall_grammar_score=result_data.get('grammar', {}).get('overall_score', None),
        overall_pronunciation_score=result_data.get('pronunciation', {}).get('overall_score', None),
        tagged_transcript=result_data.get('fluency', {}).get('feedback', {}).get('tagged_transcript', None),
        expected_text=result_data.get('pronunciation', {}).get('expected_text', None),
        user_id=x_user_id,
        question=question,
        description=description,
    )

    async with db.begin():
        db.add(main_response)
        await db.flush()  # to get the id of the inserted row
        response_id = main_response.id

        # Store pronunciation details if they exist
        if 'pronunciation' in result_data:
            pronunciation = Pronunciation(
                response_id=response_id,
                overall_score=result_data['pronunciation'].get('overall_score', None),
                lowest_scoring_phonemes=result_data['pronunciation'].get('lowest_scoring_phonemes', None)
            )
            db.add(pronunciation)

        # Store fluency details if they exist
        if 'fluency' in result_data:
            fluency = Fluency(
                response_id=response_id,
                overall_score=result_data['fluency'].get('overall_score', None),
                speech_rate=result_data['fluency'].get('metrics', {}).get('speech_rate', None),
                pauses=result_data['fluency'].get('metrics', {}).get('pauses', None),
                filler_words=result_data['fluency'].get('metrics', {}).get('filler_words', None),
                feedback_text=result_data['fluency'].get('feedback', {}).get('feedback_text', None),
                speech_rate_over_time=result_data['fluency'].get('metrics', {}).get('speech_rate_over_time', None),
                filler_words_per_min=result_data['fluency'].get('metrics', {}).get('filler_words_per_min', None)
            )
            db.add(fluency)

        # Store vocabulary details if they exist
        if 'vocabulary' in result_data:
            vocabulary = Vocabulary(
                response_id=response_id,
                overall_score=result_data['vocabulary'].get('overall_score', None),
                vocabulary_complexity=result_data['vocabulary'].get('metrics', {}).get('vocabulary_complexity', None),
                feedback_text=result_data['vocabulary'].get('feedback', {}).get('feedback_text', None)
            )
            db.add(vocabulary)

        # Store grammar details if they exist
        if 'grammar' in result_data:
            grammar = Grammar(
                response_id=response_id,
                overall_score=result_data['grammar'].get('overall_score', None),
                feedback_text=json.dumps(result_data['grammar'].get('feedback', {}))
            )
            db.add(grammar)

        # Store word-level pronunciation details if they exist
        if 'pronunciation' in result_data and 'words' in result_data['pronunciation']:
            for word in result_data['pronunciation']['words']:
                word_entry = Words(
                    response_id=response_id,
                    word_text=word.get('word_text', None),
                    word_score=word.get('word_score', None),
                    phoneme_data=word.get('phonemes', None)
                )
                db.add(word_entry)

    return {"message": "Result stored successfully", "response_id": response_id}
