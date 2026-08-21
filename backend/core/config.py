from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BuildAtlas API"
    environment: str = "development"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    gemini_api_key: str | None = None
    weather_api_key: str | None = None
    azure_vision_endpoint: str | None = None
    azure_vision_key: str | None = None
    azure_vision_api_version: str = "v3.2"
    azure_vision_submit_timeout_seconds: float = 30
    azure_vision_poll_timeout_seconds: float = 10
    azure_vision_poll_interval_seconds: float = 1
    azure_vision_max_poll_attempts: int = 60
    azure_vision_max_poll_seconds: float = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
