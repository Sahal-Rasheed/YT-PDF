from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App Config
    PROJECT_NAME: str = "YT-PDF API"
    API_V1_STR: str = "/api/v1"
    API_BASE_URL: str = "http://localhost:8000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    DEBUG: bool = True

    # CORS Config
    BACKEND_CORS_ORIGINS: list[str] = []

    # OpenAI Config
    OPENAI_API_KEY: str

    # File Storage Config
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_AUDIO_FORMATS: list[str] = ["mp3", "wav", "m4a", "webm"]

    # Processing Config
    MAX_VIDEO_DURATION: int = 7200  # 2 hours in seconds
    WHISPER_MODEL: str = "whisper-1"
    GPT_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"


settings = Settings()
