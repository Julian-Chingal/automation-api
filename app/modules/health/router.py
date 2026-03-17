from fastapi import APIRouter
from app.utils.schema import HealthResponse

router = APIRouter()

@router.post("/", response_model=HealthResponse, description="Ruta para checar el estado del servicio")
async def health_check():
    try:
        return HealthResponse(
            status=True,
            message="Servicio funcionando correctamente",
        )
    except Exception as e:
        return HealthResponse(
            status=False,
            message=str(e),
        )