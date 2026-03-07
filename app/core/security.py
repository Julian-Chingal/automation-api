from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from .settings import settings
import secrets

api_key_header = APIKeyHeader(
    name=settings.SECURITY_API_KEY_HEADER,
    scheme_name=settings.SECURITY_API_KEY_HEADER_DESCRIPTION,
    description=settings.SECURITY_SCHEME_NAME,
    auto_error=False
)

def api_key_auth(api_key: str = Security(api_key_header)):
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
            headers={"WWW-Authenticate": "ApiKeyAuth"},
        )
    
    if not secrets.compare_digest(api_key, settings.SECURITY_DEFAULT_API_KEY.get_secret_value()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
            headers={"WWW-Authenticate": "ApiKeyAuth"},
        )

    return api_key