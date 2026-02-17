from fastapi import APIRouter
from modules.ERC.router import router as erc_router


api_router = APIRouter()

api_router.include_router(erc_router, prefix="/v1/erc", tags=["ERC"])

