from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Clarivo API"
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    web_origin: str = "http://localhost:3000"
    database_url: str = (
        "postgresql+psycopg://clarivo:clarivo@localhost:5433/clarivo"
    )
    s3_endpoint: str = "http://localhost:9000"
    s3_bucket: str = "clarivo-audio"
    s3_access_key: str = "clarivo"
    s3_secret_key: str = "clarivo-local-secret"
    s3_region: str = "us-east-1"
    max_audio_bytes: int = 25 * 1024 * 1024

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
