from pydantic_settings import BaseSettings
from typing import List, Literal, Optional
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv(override=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dino Encyclopedia API"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5174"]  # Agregamos ambas variantes
    
    # Server configuration
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "127.0.0.1")  # Cambiado de 0.0.0.0 a 127.0.0.1
    ENVIRONMENT: Literal["development", "production", "testing"] = os.getenv("ENVIRONMENT", "development")
    
    # Firebase configuration
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_PRIVATE_KEY_ID: str = os.getenv("FIREBASE_PRIVATE_KEY_ID", "")
    FIREBASE_PRIVATE_KEY: str = os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n')
    FIREBASE_CLIENT_EMAIL: str = os.getenv("FIREBASE_CLIENT_EMAIL", "")
    FIREBASE_CLIENT_ID: str = os.getenv("FIREBASE_CLIENT_ID", "")
    FIREBASE_CLIENT_CERT_URL: str = os.getenv("FIREBASE_CLIENT_CERT_URL", "")
    FIREBASE_WEB_API_KEY: str = os.getenv("FIREBASE_WEB_API_KEY", "")
    
    # Supabase configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # SendGrid configuration
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER", "")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

# Para debugging
print("FIREBASE_PROJECT_ID:", os.getenv("FIREBASE_PROJECT_ID"))

settings = Settings() 