from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from app.core.logger import logger

class Settings(BaseSettings):
    DATABASE_URL: str
    LANGUAGE_MODEL_PROVIDER: str
    LANGUAGE_MODEL_API_KEY: str
    LANGUAGE_MODEL_TYPE: str
    SECRET_KEY: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
logger.info("Settings loaded successfully.")
