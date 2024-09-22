from celery.bin.upgrade import settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VIRUSTOTAL_API_KEY: str
    MONGO_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"  # This tells Pydantic to load variables from .env
settings()