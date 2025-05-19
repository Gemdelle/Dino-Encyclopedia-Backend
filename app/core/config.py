from pydantic_settings import BaseSettings
from typing import List, Literal, Optional
import os
from dotenv import load_dotenv

# Asegurarse de que .env se carga
load_dotenv(override=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dino Encyclopedia API"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ]
    
    # Server configuration
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "development"
    
    # Firebase configuration
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_CLIENT_ID: str
    FIREBASE_CLIENT_CERT_URL: str
    FIREBASE_WEB_API_KEY: str
    
    # Supabase configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.FIREBASE_PRIVATE_KEY:
            self.FIREBASE_PRIVATE_KEY = self.FIREBASE_PRIVATE_KEY.replace('\\n', '\n')

settings = Settings()

# Para debugging
print("Loaded settings:")
print(f"FIREBASE_PROJECT_ID: {settings.FIREBASE_PROJECT_ID}")
print(f"SUPABASE_URL: {settings.SUPABASE_URL}") 