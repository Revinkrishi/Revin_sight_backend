from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB: str

    # multiple device keys
    VALID_DEVICE_KEYS: str
    
    STATIC_API_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()

# Make list from comma-separated string
DEVICE_KEY_LIST = [key.strip() for key in settings.VALID_DEVICE_KEYS.split(",")]

