from fastapi import APIRouter
from app.modules.erc.router import router as erc_router
from app.modules.ep.router import router as ep_router
from app.modules.health.router import router as health_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(erc_router, prefix="/erc", tags=["Estados de Relaciones Comerciales"])
api_router.include_router(ep_router, prefix="/ep", tags=["Ejecución Presupuestal"])


