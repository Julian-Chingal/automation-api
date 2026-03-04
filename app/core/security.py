from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import secrets
import os 

api_key_header = APIKeyHeader(
    name=str(os.getenv("SECURITY_API_KEY_HEADER")),
    scheme_name=str(os.getenv("SECURITY_API_KEY_HEADER_DESCRIPTION")),
    description=str(os.getenv("SECURITY_SCHEME_NAME")),
    auto_error=False
)

def api_key_auth(api_key: str = Security(api_key_header)):
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
            headers={"WWW-Authenticate": "ApiKeyAuth"},
        )
    
    if not secrets.compare_digest(api_key, os.getenv("SECURITY_DEFAULT_API_KEY")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
            headers={"WWW-Authenticate": "ApiKeyAuth"},
        )

    return api_key