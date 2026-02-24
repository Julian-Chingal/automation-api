from fastapi import APIRouter
from modules.erc.router import router as erc_router

api_router = APIRouter()

api_router.include_router(erc_router, prefix="/erc", tags=["ERC"])

