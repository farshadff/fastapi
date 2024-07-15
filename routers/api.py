from fastapi import APIRouter, UploadFile, File
from services.audio_service import process_audio_file

router = APIRouter()


@router.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    response = await process_audio_file(file)
    return response
