from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Mi Tienda API"
    API_V1_STR: str = "/api/v1"

    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    FIREBASE_PROJECT_ID: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()