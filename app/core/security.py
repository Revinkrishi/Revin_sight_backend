from fastapi import HTTPException, Header
from app.core.config import DEVICE_KEY_LIST
from app.core.config import settings

def validate_query_api_key(input_key: str):
    print("\n===== API KEY VALIDATION DEBUG START =====", flush=True)
    print("API Key Received:", input_key, flush=True)
    # print("Valid API Keys:", DEVICE_KEY_LIST, flush=True)

    if not input_key:
        print("❌ ERROR: No API key provided", flush=True)
        print("===== API KEY VALIDATION DEBUG END =====\n", flush=True)
        raise HTTPException(400, "API_KEY is required")

    if input_key not in DEVICE_KEY_LIST:
        print("❌ ERROR: Invalid API key", flush=True)
        print("===== API KEY VALIDATION DEBUG END =====\n", flush=True)
        raise HTTPException(401, "Invalid API_KEY")

    print("✔ API key validation PASSED", flush=True)
    print("===== API KEY VALIDATION DEBUG END =====\n", flush=True)


def verify_static_token(authorization: str = Header(None)):
    print("\n===== STATIC TOKEN DEBUG START =====", flush=True)
    print("Authorization header received:", authorization, flush=True)

    if authorization is None:
        print("❌ ERROR: No Authorization header", flush=True)
        print("===== STATIC TOKEN DEBUG END =====\n", flush=True)
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        print("❌ ERROR: Invalid header format", flush=True)
        print("===== STATIC TOKEN DEBUG END =====\n", flush=True)
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.split("Bearer ")[1].strip()
    print("Extracted token:", token, flush=True)
    # print("Expected token:", settings.STATIC_API_TOKEN, flush=True)

    if token != settings.STATIC_API_TOKEN:
        print("❌ ERROR: Token mismatch", flush=True)
        print("===== STATIC TOKEN DEBUG END =====\n", flush=True)
        raise HTTPException(status_code=401, detail="Invalid API token")

    print("✔ Static token validation PASSED", flush=True)
    print("===== STATIC TOKEN DEBUG END =====\n", flush=True)
    return True
