from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.audio_service import process_audio_file
from database import get_db

router = APIRouter()

@router.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    response = await process_audio_file(file, db)
    return response
