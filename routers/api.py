from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.accent_service import process_accent_file
from services.audio_service import process_audio_file
from database import get_db

router = APIRouter()


@router.post("/upload-audio/")
async def upload_audio(
        file: UploadFile = File(...),
        user_id: str = Form(...),
        speaker_gender: str = Form("speaker_gender"),
        speaker_age: str = Form("speaker_age"),
        question: str = Form("question"),
        description: str = Form("description"),
        db: AsyncSession = Depends(get_db)

):
    response = await process_audio_file(file, user_id, speaker_gender, speaker_age, question, description, db)
    return response


@router.post("/accent-service/")
async def upload_accent_audio(
        file: UploadFile = File(...),
        user_id: str = Form(...),
        speaker_gender: str = Form("speaker_gender"),
        speaker_age: str = Form("speaker_age"),
        question: str = Form("question"),
        description: str = Form("description"),
        expected_text: str = Form(...),  # New parameter to accept expected text from the user
        db: AsyncSession = Depends(get_db)

):
    response = await process_accent_file(file, user_id, speaker_gender, speaker_age, question, description,expected_text, db)
    return response
