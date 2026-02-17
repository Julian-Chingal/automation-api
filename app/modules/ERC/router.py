from fastapi import APIRouter

router = APIRouter()

@router.post("/bienes")
async def read_erc():
    return {"message": "Hello from ERC Bienes"}

@router.post("/servicios")
async def read_erc():
    return {"message": "Hello from ERC Servicios"}

@router.post("/inversion")
async def read_erc():
    return {"message": "Hello from ERC Inversion"}

@router.post("/turismo")
async def read_erc():
    return {"message": "Hello from ERC Turismo"}

@router.post("/configuracion")
async def read_erc():
    return {"message": "Hello from ERC Configuracion"}