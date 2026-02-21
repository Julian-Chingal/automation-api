from fastapi import APIRouter

from .turismo_router import router as turismo_router

router = APIRouter()

router.include_router(turismo_router)

@router.post("/bienes")
async def post_bienes():
    return {"message": "Lista de bienes"}

@router.post("/servicios")
async def post_servicios():
    return {"message": "Lista de servicios"}

@router.post("/inversion")
async def post_inversion():
    return {"message": "Lista de inversiones"}


@router.post("/configuracion")
async def post_configuracion():
    return {"message": "Configuración de ERC"}
