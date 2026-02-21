from fastapi import APIRouter
from transformers import TurismoTransformer

router = APIRouter()

@router.post("/bienes")
async def post_bienes():
    return {"message": "Lista de bienes"}

@router.post("/servicios")
async def post_servicios():
    return {"message": "Lista de servicios"}

@router.post("/inversion")
async def post_inversion():
    return {"message": "Lista de inversiones"}

@router.post("/turismo")
async def post_turismo():
    return {"message": "Lista de turismo"}

@router.post("/configuracion")
async def post_configuracion():
    return {"message": "Configuración de ERC"}