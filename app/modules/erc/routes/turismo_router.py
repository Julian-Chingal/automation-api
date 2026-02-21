from fastapi import APIRouter, Depends, File, Request, UploadFile

from ..schema import UploadResponse
from ..services.turismo_uploader import upload_turismo
from utils.loader_file import load_file

router = APIRouter()

def get_db_manager(request: Request):
    return request.app.state.db_manager

@router.post("/turismo",response_model=UploadResponse)
async def upload_turismo_endpoint():
    return {"message": "Upload successful"}
