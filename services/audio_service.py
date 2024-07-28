import time
from datetime import datetime

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from typing import Any
from models import ServiceResult
import base64
import requests
from database import database
import time
from datetime import datetime

from fastapi import UploadFile, APIRouter
from pydantic import BaseModel
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from models import MainResponse, Pronunciation, Fluency, Vocabulary, Grammar, Words
import base64
from database import database

router = APIRouter()

# Mocked response data
MOCKED_RESPONSE_DATA = {
    "pronunciation": {
        "words": [
            {
                "word_text": "Okay",
                "phonemes": [
                    {"ipa_label": "oʊ", "phoneme_score": 100},
                    {"ipa_label": "k", "phoneme_score": 100},
                    {"ipa_label": "eɪ", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "I",
                "phonemes": [{"ipa_label": "aɪ", "phoneme_score": 100}],
                "word_score": 100
            },
            {
                "word_text": "think",
                "phonemes": [
                    {"ipa_label": "θ", "phoneme_score": 40},
                    {"ipa_label": "ɪ", "phoneme_score": 100},
                    {"ipa_label": "ŋ", "phoneme_score": 100},
                    {"ipa_label": "k", "phoneme_score": 100}
                ],
                "word_score": 85
            },
            {
                "word_text": "the",
                "phonemes": [
                    {"ipa_label": "ð", "phoneme_score": 0},
                    {"ipa_label": "i", "phoneme_score": 100}
                ],
                "word_score": 50
            },
            {
                "word_text": "advancement",
                "phonemes": [
                    {"ipa_label": "ə", "phoneme_score": 0},
                    {"ipa_label": "d", "phoneme_score": 100},
                    {"ipa_label": "v", "phoneme_score": 100},
                    {"ipa_label": "æ", "phoneme_score": 100},
                    {"ipa_label": "n", "phoneme_score": 50},
                    {"ipa_label": "s", "phoneme_score": 100},
                    {"ipa_label": "m", "phoneme_score": 0},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "n", "phoneme_score": 100},
                    {"ipa_label": "t", "phoneme_score": 100}
                ],
                "word_score": 75
            },
            {
                "word_text": "of",
                "phonemes": [
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "v", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "technology",
                "phonemes": [
                    {"ipa_label": "t", "phoneme_score": 0},
                    {"ipa_label": "ɛ", "phoneme_score": 0},
                    {"ipa_label": "k", "phoneme_score": 100},
                    {"ipa_label": "n", "phoneme_score": 100},
                    {"ipa_label": "ɑ", "phoneme_score": 40},
                    {"ipa_label": "l", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "d", "phoneme_score": 100},
                    {"ipa_label": "ʒ", "phoneme_score": 100},
                    {"ipa_label": "i", "phoneme_score": 100}
                ],
                "word_score": 74
            },
            {
                "word_text": "is",
                "phonemes": [
                    {"ipa_label": "ɪ", "phoneme_score": 100},
                    {"ipa_label": "z", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "a",
                "phonemes": [{"ipa_label": "ə", "phoneme_score": 100}],
                "word_score": 100
            },
            {
                "word_text": "good",
                "phonemes": [
                    {"ipa_label": "g", "phoneme_score": 100},
                    {"ipa_label": "ʊ", "phoneme_score": 49},
                    {"ipa_label": "d", "phoneme_score": 100}
                ],
                "word_score": 83
            },
            {
                "word_text": "development",
                "phonemes": [
                    {"ipa_label": "d", "phoneme_score": 42},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "v", "phoneme_score": 0},
                    {"ipa_label": "ɛ", "phoneme_score": 42},
                    {"ipa_label": "l", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "p", "phoneme_score": 100},
                    {"ipa_label": "m", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "n", "phoneme_score": 100},
                    {"ipa_label": "t", "phoneme_score": 100}
                ],
                "word_score": 80
            },
            {
                "word_text": "for",
                "phonemes": [
                    {"ipa_label": "f", "phoneme_score": 100},
                    {"ipa_label": "ɔ", "phoneme_score": 100},
                    {"ipa_label": "r", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "people",
                "phonemes": [
                    {"ipa_label": "p", "phoneme_score": 90},
                    {"ipa_label": "i", "phoneme_score": 100},
                    {"ipa_label": "p", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "l", "phoneme_score": 100}
                ],
                "word_score": 98
            },
            {
                "word_text": "I",
                "phonemes": [{"ipa_label": "aɪ", "phoneme_score": 0}],
                "word_score": 0
            },
            {
                "word_text": "think",
                "phonemes": [
                    {"ipa_label": "θ", "phoneme_score": 87},
                    {"ipa_label": "ɪ", "phoneme_score": 100},
                    {"ipa_label": "ŋ", "phoneme_score": 100},
                    {"ipa_label": "k", "phoneme_score": 100}
                ],
                "word_score": 96
            },
            {
                "word_text": "every",
                "phonemes": [
                    {"ipa_label": "ɛ", "phoneme_score": 0},
                    {"ipa_label": "v", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "r", "phoneme_score": 100},
                    {"ipa_label": "i", "phoneme_score": 100}
                ],
                "word_score": 80
            },
            {
                "word_text": "person",
                "phonemes": [
                    {"ipa_label": "p", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "r", "phoneme_score": 100},
                    {"ipa_label": "s", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 44},
                    {"ipa_label": "n", "phoneme_score": 100}
                ],
                "word_score": 90
            },
            {
                "word_text": "on",
                "phonemes": [
                    {"ipa_label": "ɔ", "phoneme_score": 100},
                    {"ipa_label": "n", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "this",
                "phonemes": [
                    {"ipa_label": "ð", "phoneme_score": 47},
                    {"ipa_label": "ɪ", "phoneme_score": 100},
                    {"ipa_label": "s", "phoneme_score": 100}
                ],
                "word_score": 82
            },
            {
                "word_text": "board",
                "phonemes": [
                    {"ipa_label": "b", "phoneme_score": 0},
                    {"ipa_label": "ɔ", "phoneme_score": 100},
                    {"ipa_label": "r", "phoneme_score": 100},
                    {"ipa_label": "d", "phoneme_score": 100}
                ],
                "word_score": 75
            },
            {
                "word_text": "have",
                "phonemes": [
                    {"ipa_label": "h", "phoneme_score": 0},
                    {"ipa_label": "æ", "phoneme_score": 89},
                    {"ipa_label": "v", "phoneme_score": 100}
                ],
                "word_score": 63
            },
            {
                "word_text": "the",
                "phonemes": [
                    {"ipa_label": "ð", "phoneme_score": 100},
                    {"ipa_label": "i", "phoneme_score": 40}
                ],
                "word_score": 70
            },
            {
                "word_text": "right",
                "phonemes": [
                    {"ipa_label": "r", "phoneme_score": 0},
                    {"ipa_label": "aɪ", "phoneme_score": 0},
                    {"ipa_label": "t", "phoneme_score": 0}
                ],
                "word_score": 0
            },
            {
                "word_text": "to",
                "phonemes": [
                    {"ipa_label": "t", "phoneme_score": 0},
                    {"ipa_label": "u", "phoneme_score": 40}
                ],
                "word_score": 20
            },
            {
                "word_text": "have",
                "phonemes": [
                    {"ipa_label": "h", "phoneme_score": 0},
                    {"ipa_label": "æ", "phoneme_score": 40},
                    {"ipa_label": "v", "phoneme_score": 40}
                ],
                "word_score": 26
            },
            {
                "word_text": "access",
                "phonemes": [
                    {"ipa_label": "æ", "phoneme_score": 0},
                    {"ipa_label": "k", "phoneme_score": 40},
                    {"ipa_label": "s", "phoneme_score": 100},
                    {"ipa_label": "ɛ", "phoneme_score": 0},
                    {"ipa_label": "s", "phoneme_score": 100}
                ],
                "word_score": 48
            },
            {
                "word_text": "to",
                "phonemes": [
                    {"ipa_label": "t", "phoneme_score": 100},
                    {"ipa_label": "u", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "good",
                "phonemes": [
                    {"ipa_label": "g", "phoneme_score": 0},
                    {"ipa_label": "ʊ", "phoneme_score": 43},
                    {"ipa_label": "d", "phoneme_score": 100}
                ],
                "word_score": 47
            },
            {
                "word_text": "technologies",
                "phonemes": [
                    {"ipa_label": "t", "phoneme_score": 0},
                    {"ipa_label": "ɛ", "phoneme_score": 0},
                    {"ipa_label": "k", "phoneme_score": 100},
                    {"ipa_label": "n", "phoneme_score": 100},
                    {"ipa_label": "ɑ", "phoneme_score": 0},
                    {"ipa_label": "l", "phoneme_score": 0},
                    {"ipa_label": "ə", "phoneme_score": 88},
                    {"ipa_label": "d", "phoneme_score": 0},
                    {"ipa_label": "ʒ", "phoneme_score": 100},
                    {"ipa_label": "i", "phoneme_score": 0},
                    {"ipa_label": "z", "phoneme_score": 0}
                ],
                "word_score": 35
            },
            {
                "word_text": "But",
                "phonemes": [
                    {"ipa_label": "b", "phoneme_score": 0},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "t", "phoneme_score": 100}
                ],
                "word_score": 66
            },
            {
                "word_text": "there",
                "phonemes": [
                    {"ipa_label": "ð", "phoneme_score": 45},
                    {"ipa_label": "ɛ", "phoneme_score": 100},
                    {"ipa_label": "r", "phoneme_score": 100}
                ],
                "word_score": 81
            },
            {
                "word_text": "are",
                "phonemes": [
                    {"ipa_label": "ɑ", "phoneme_score": 100},
                    {"ipa_label": "r", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "several",
                "phonemes": [
                    {"ipa_label": "s", "phoneme_score": 100},
                    {"ipa_label": "ɛ", "phoneme_score": 100},
                    {"ipa_label": "v", "phoneme_score": 42},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "r", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "l", "phoneme_score": 100}
                ],
                "word_score": 91
            },
            {
                "word_text": "disadvantages",
                "phonemes": [
                    {"ipa_label": "d", "phoneme_score": 100},
                    {"ipa_label": "ɪ", "phoneme_score": 0},
                    {"ipa_label": "s", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "d", "phoneme_score": 100},
                    {"ipa_label": "v", "phoneme_score": 3},
                    {"ipa_label": "æ", "phoneme_score": 0},
                    {"ipa_label": "n", "phoneme_score": 100},
                    {"ipa_label": "t", "phoneme_score": 100},
                    {"ipa_label": "ɪ", "phoneme_score": 100},
                    {"ipa_label": "d", "phoneme_score": 100},
                    {"ipa_label": "ʒ", "phoneme_score": 100},
                    {"ipa_label": "z", "phoneme_score": 0}
                ],
                "word_score": 69
            },
            {
                "word_text": "for",
                "phonemes": [
                    {"ipa_label": "f", "phoneme_score": 0},
                    {"ipa_label": "ɔ", "phoneme_score": 100},
                    {"ipa_label": "r", "phoneme_score": 100}
                ],
                "word_score": 66
            },
            {
                "word_text": "this",
                "phonemes": [
                    {"ipa_label": "ð", "phoneme_score": 89},
                    {"ipa_label": "ɪ", "phoneme_score": 100},
                    {"ipa_label": "s", "phoneme_score": 100}
                ],
                "word_score": 96
            },
            {
                "word_text": "I",
                "phonemes": [{"ipa_label": "aɪ", "phoneme_score": 0}],
                "word_score": 0
            },
            {
                "word_text": "I",
                "phonemes": [{"ipa_label": "aɪ", "phoneme_score": 100}],
                "word_score": 100
            },
            {
                "word_text": "I",
                "phonemes": [{"ipa_label": "aɪ", "phoneme_score": 0}],
                "word_score": 0
            },
            {
                "word_text": "mean",
                "phonemes": [
                    {"ipa_label": "m", "phoneme_score": 100},
                    {"ipa_label": "i", "phoneme_score": 0},
                    {"ipa_label": "n", "phoneme_score": 100}
                ],
                "word_score": 66
            },
            {
                "word_text": "I",
                "phonemes": [{"ipa_label": "aɪ", "phoneme_score": 100}],
                "word_score": 100
            },
            {
                "word_text": "mean",
                "phonemes": [
                    {"ipa_label": "m", "phoneme_score": 100},
                    {"ipa_label": "i", "phoneme_score": 48},
                    {"ipa_label": "n", "phoneme_score": 100}
                ],
                "word_score": 82
            },
            {
                "word_text": "however",
                "phonemes": [
                    {"ipa_label": "h", "phoneme_score": 0},
                    {"ipa_label": "aʊ", "phoneme_score": 100},
                    {"ipa_label": "ɛ", "phoneme_score": 0},
                    {"ipa_label": "v", "phoneme_score": 48},
                    {"ipa_label": "ə", "phoneme_score": 0},
                    {"ipa_label": "r", "phoneme_score": 100}
                ],
                "word_score": 41
            },
            {
                "word_text": "there",
                "phonemes": [
                    {"ipa_label": "ð", "phoneme_score": 0},
                    {"ipa_label": "ɛ", "phoneme_score": 3},
                    {"ipa_label": "r", "phoneme_score": 100}
                ],
                "word_score": 34
            },
            {
                "word_text": "are",
                "phonemes": [
                    {"ipa_label": "ɑ", "phoneme_score": 48},
                    {"ipa_label": "r", "phoneme_score": 100}
                ],
                "word_score": 74
            },
            {
                "word_text": "so",
                "phonemes": [
                    {"ipa_label": "s", "phoneme_score": 100},
                    {"ipa_label": "oʊ", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "many",
                "phonemes": [
                    {"ipa_label": "m", "phoneme_score": 100},
                    {"ipa_label": "ɛ", "phoneme_score": 100},
                    {"ipa_label": "n", "phoneme_score": 100},
                    {"ipa_label": "i", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "problems",
                "phonemes": [
                    {"ipa_label": "p", "phoneme_score": 100},
                    {"ipa_label": "r", "phoneme_score": 100},
                    {"ipa_label": "ɑ", "phoneme_score": 100},
                    {"ipa_label": "b", "phoneme_score": 100},
                    {"ipa_label": "l", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 100},
                    {"ipa_label": "m", "phoneme_score": 100},
                    {"ipa_label": "z", "phoneme_score": 54}
                ],
                "word_score": 94
            },
            {
                "word_text": "with",
                "phonemes": [
                    {"ipa_label": "w", "phoneme_score": 100},
                    {"ipa_label": "ɪ", "phoneme_score": 43},
                    {"ipa_label": "ð", "phoneme_score": 100}
                ],
                "word_score": 81
            },
            {
                "word_text": "new",
                "phonemes": [
                    {"ipa_label": "n", "phoneme_score": 100},
                    {"ipa_label": "u", "phoneme_score": 100}
                ],
                "word_score": 100
            },
            {
                "word_text": "technology",
                "phonemes": [
                    {"ipa_label": "t", "phoneme_score": 89},
                    {"ipa_label": "ɛ", "phoneme_score": 40},
                    {"ipa_label": "k", "phoneme_score": 100},
                    {"ipa_label": "n", "phoneme_score": 100},
                    {"ipa_label": "ɑ", "phoneme_score": 0},
                    {"ipa_label": "l", "phoneme_score": 100},
                    {"ipa_label": "ə", "phoneme_score": 49},
                    {"ipa_label": "d", "phoneme_score": 100},
                    {"ipa_label": "ʒ", "phoneme_score": 100},
                    {"ipa_label": "i", "phoneme_score": 0}
                ],
                "word_score": 67
            }
        ],
        "overall_score": 54.5,
        "expected_text": "Okay. I think the advancement of technology is a good development for people. I think every person on this board have the right to, have access to good technologies. But, there are several disadvantages for this. I, I I mean, I mean, however, there are so many problems with new technology",
        "english_proficiency_scores": {
            "mock_ielts": {"prediction": 6},
            "mock_cefr": {"prediction": "C1"},
            "mock_pte": {"prediction": 84}
        },
        "warnings": {},
        "lowest_scoring_phonemes": [
            {"ipa_label": "j", "phoneme_score": 0},
            {"ipa_label": "ð", "phoneme_score": 0},
            {"ipa_label": "ɛ", "phoneme_score": 21}
        ]
    },
    "fluency": {
        "overall_score": 68,
        "metrics": {
            "speech_rate": 103,
            "speech_rate_over_time": [80, 180, 80, 120, 80, 80, 100, 60, 80, 80, 140, 121],
            "pauses": 2,
            "filler_words": 4,
            "discourse_markers": None,
            "filler_words_per_min": 8,
            "pause_details": None,
            "repetitions": None,
            "filler_words_details": None
        },
        "english_proficiency_scores": {
            "mock_ielts": {"prediction": 7},
            "mock_cefr": {"prediction": "B2"},
            "mock_pte": {"prediction": 66}
        },
        "warnings": {},
        "feedback": {
            "speech_rate": {"feedback_code": "NORMAL", "feedback_text": "You are speaking at a normal pace."},
            "pauses": {"feedback_code": "SOME_PAUSES",
                       "feedback_text": "You are making some long pauses when you speak. Try to make shorter pauses in between your sentences."},
            "filler_words": {"feedback_code": "SOME_FILLER_WORDS",
                             "feedback_text": "You are using some filler words when you speak. Try to avoid using filler words."},
            "tagged_transcript": "Okay. Uh, I think the advancement of technology is a good development for people. I think every person on this board have the right to, uh, have access to good technologies. But, uh, there are several disadvantages for this. I, uh, I I mean, I mean, however, there are so many problems with new technology"
        }
    },
    "overall": {
        "english_proficiency_scores": {
            "mock_ielts": {"prediction": 7.5},
            "mock_cefr": {"prediction": "C1"},
            "mock_pte": {"prediction": 76}
        },
        "overall_score": 72
    },
    "warnings": {},
    "vocabulary": {
        "overall_score": 76,
        "metrics": {"vocabulary_complexity": "AVERAGE", "idiom_details": []},
        "english_proficiency_scores": {
            "mock_ielts": {"prediction": 7.5},
            "mock_cefr": {"prediction": "C1"},
            "mock_pte": {"prediction": "76"}
        },
        "warnings": {},
        "feedback": {
            "tagged_transcript": "Okay. Uh, I think the advancement of technology is a good development for people. I think every person on this board have the right to, uh, have access to good technologies. But, uh, there are several disadvantages for this. I, uh, I I mean, I mean, however, there are so many problems with new technology"
        }
    },
    "grammar": {
        "overall_score": 90,
        "metrics": None,
        "english_proficiency_scores": {
            "mock_ielts": {"prediction": 9},
            "mock_cefr": {"prediction": "C2"},
            "mock_pte": {"prediction": 89}
        },
        "feedback": None
    },
    "metadata": {
        "predicted_text": "Okay. Uh, I think the advancement of technology is a good development for people. I think every person on this board have the right to, uh, have access to good technologies. But, uh, there are several disadvantages for this. I, uh, I I mean, I mean, however, there are so many problems with new technology",
        "content_relevance": None,
        "content_relevance_feedback": None,
        "valid_answer": None
    }
}


class ServiceResultCreate(BaseModel):
    user: str
    type: str
    result: Any
    date_fa: str


async def read_file_as_base64(file: UploadFile) -> str:
    content = await file.read()
    return base64.b64encode(content).decode('utf-8')


# @app.post("/process_audio/")
async def process_audio_file(file: UploadFile, db: AsyncSession):
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
        expected_text=result_data['pronunciation'].get('expected_text', '')
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
            feedback_text=result_data['grammar'].get('feedback', '')
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
