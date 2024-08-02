from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.audio_service import process_audio_file
from database import get_db

router = APIRouter()

@router.post("/upload-audio/")
async def upload_audio(
    file: UploadFile = File(...),
    x_user_id: str = Form("user_id"),
    speaker_gender: str = Form("speaker_gender"),
    speaker_age: str = Form("speaker_age"),

):
    response = await process_audio_file(file, x_user_id, speaker_gender, speaker_age)
    return response