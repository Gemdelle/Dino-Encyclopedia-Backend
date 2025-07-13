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
    
    # Railway domain (will be added to ALLOWED_ORIGINS if provided)
    RAILWAY_DOMAIN: Optional[str] = None
    
    # Server configuration
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Firebase configuration
    FIREBASE_PROJECT_ID: Optional[str] = None
    FIREBASE_PRIVATE_KEY_ID: Optional[str] = None
    FIREBASE_PRIVATE_KEY: Optional[str] = None
    FIREBASE_CLIENT_EMAIL: Optional[str] = None
    FIREBASE_CLIENT_ID: Optional[str] = None
    FIREBASE_CLIENT_CERT_URL: Optional[str] = None
    FIREBASE_WEB_API_KEY: Optional[str] = None
    
    # Supabase configuration
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.FIREBASE_PRIVATE_KEY:
            self.FIREBASE_PRIVATE_KEY = self.FIREBASE_PRIVATE_KEY.replace('\\n', '\n')
        
        # Agregar dominio de Railway a los orígenes permitidos si está configurado
        if self.RAILWAY_DOMAIN:
            if self.RAILWAY_DOMAIN not in self.ALLOWED_ORIGINS:
                self.ALLOWED_ORIGINS.append(self.RAILWAY_DOMAIN)
        
        # Validar que las variables requeridas estén presentes en producción
        if self.ENVIRONMENT != "development":
            if not all([
                self.FIREBASE_PROJECT_ID,
                self.FIREBASE_PRIVATE_KEY_ID,
                self.FIREBASE_PRIVATE_KEY,
                self.FIREBASE_CLIENT_EMAIL,
                self.FIREBASE_CLIENT_ID,
                self.FIREBASE_CLIENT_CERT_URL,
                self.FIREBASE_WEB_API_KEY,
                self.SUPABASE_URL,
                self.SUPABASE_KEY
            ]):
                raise ValueError("All environment variables are required in production mode")

settings = Settings()

# Para debugging solo en desarrollo
if settings.ENVIRONMENT == "development":
    print("Loaded settings:")
    print(f"FIREBASE_PROJECT_ID: {settings.FIREBASE_PROJECT_ID}")
    print(f"SUPABASE_URL: {settings.SUPABASE_URL}") 