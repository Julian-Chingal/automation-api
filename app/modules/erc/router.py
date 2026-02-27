from fastapi import APIRouter, Depends, File, Request, UploadFile

from .schema import UploadResponse
from .service import (
    turismo_service,
    inversion_service,
    servicios_service
    )
from utils.loader_file import load_file

router = APIRouter()

def get_db_manager(request: Request):
    return request.app.state.db_manager

@router.post("/turismo",response_model=UploadResponse, description= "Ruta para actualizar los datos de turismo" )
async def upload_turismo(
    file: UploadFile = File(...),
    db_manager= Depends(get_db_manager)
):
    df = await load_file(file)
    rows = turismo_service(df, db_manager)

    return {
        "status": True,
        "message": "Se actualizo el registro de turismo",
        "rows_uploaded": rows,
        "destination_table": "visitas_turismo"
    }

@router.post("/inversion", response_model=UploadResponse, description="Ruta para actualizar los datos de inversion")
async def upload_inversion(
    file: UploadFile = File(...),
    db_manager = Depends(get_db_manager)
):
    df = await load_file(file)
    rows = inversion_service(df, db_manager)

    return {
        "status": True,
        "message": "Se actualizo el registro de inversion",
        "rows_uploaded": rows,
        "destination_table": "ban_rep_inversion"
    }

@router.post("/servicios", response_model=UploadResponse, description="Ruta para actualizar los datos de servicios")
async def upload_servicios(
    file: UploadFile = File(...),
    db_manager = Depends(get_db_manager)
):
    df = await load_file(file)
    rows = servicios_service(df, db_manager)

    return {
        "status": True,
        "message": "Se actualizo el registro de servicios",
        "rows_uploaded": rows,
        "destination_table": "emces_servicios"
    }