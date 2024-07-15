import base64
from fastapi import UploadFile


async def read_file_as_base64(file: UploadFile):
    contents = await file.read()
    file_base64 = base64.b64encode(contents).decode('utf-8')
    return file_base64
