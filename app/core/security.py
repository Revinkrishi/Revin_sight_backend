from fastapi import HTTPException, Header
from app.core.config import DEVICE_KEY_LIST
from app.core.config import settings

def validate_query_api_key(input_key: str):
    if not input_key:
        raise HTTPException(400, "API_KEY is required")

    if input_key not in DEVICE_KEY_LIST:
        raise HTTPException(401, "Invalid API_KEY")



def verify_static_token(authorization: str = Header(None)):
    """
    Expected header:
    Authorization: Bearer <TOKEN>
    """
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.split("Bearer ")[1].strip()

    if token != settings.STATIC_API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")