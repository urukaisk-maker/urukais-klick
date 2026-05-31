"""
Configuración central de la aplicación
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Urukais Klick"
    
    # Seguridad
    SECRET_KEY: str = "urukais-secret-key-dev"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días
    
    # Base de datos
    DATABASE_URL: str = "postgresql://urukais:urukais123@localhost:5432/urukais_klick"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Meilisearch
    MEILISEARCH_URL: str = "http://localhost:7700"
    MEILISEARCH_API_KEY: str = ""
    
    # MinIO (S3-compatible)
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "urukais"
    MINIO_SECRET_KEY: str = "urukais123"
    MINIO_BUCKET: str = "urukais-audio"
    
    # YouTube API
    YOUTUBE_API_KEY: str = "AIzaSyDm7cm8O9VeNUWfJvooXxUdEEcugzonVjU"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"

settings = Settings()
