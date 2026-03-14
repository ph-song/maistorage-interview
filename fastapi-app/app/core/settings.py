from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from app.core.logger import logger

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app/database/database.db"
    LANGUAGE_MODEL_PROVIDER: str = "google_genai"
    LANGUAGE_MODEL_TYPE: str = "gemini-2.5-flash"
    LANGUAGE_MODEL_API_KEY: str
    SECRET_KEY: str = "supersecretkey"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
logger.info("Settings loaded successfully.")
