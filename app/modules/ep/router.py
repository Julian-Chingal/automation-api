from fastapi import APIRouter, Depends, File, Request, UploadFile
from utils.schema import UploadResponse
from .service import ejecucion_presupuestal_service

router = APIRouter()

def get_db_manager(request: Request):
    return request.app.state.db_manager

@router.post(
        "/upload", 
        response_model=UploadResponse, 
        description="Carga archivo de Ejecución Presupuestal con múltiples entidades por hoja"
)
async def upload_ejecucion_presupuestal(
    file: UploadFile = File(...),
    db_manager = Depends(get_db_manager)
):
    results = await ejecucion_presupuestal_service(file, db_manager)
    total_rows = sum(results.values())
    sheets_summary = [
        {"sheet": sheet, "rows_uploaded": rows}
        for sheet, rows in results.items()
    ]
    
    return {
        "status": True,
        "message": f"Procesadas {len(results)} entidades",
        "rows_uploaded": total_rows,
        "destination_table": "ejecucion_presupuestal",
        "detail": sheets_summary,
    }
