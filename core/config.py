from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env usando python-dotenv
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Mi Tienda API"
    API_V1_STR: str = "/api/v1"

    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    FIREBASE_PROJECT_ID: Optional[str] = None

    # Configuración SMTP para envío de correos
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: Optional[str] = None
    SMTP_TLS: bool = True

    class Config:
        env_file = ".env"

settings = Settings()