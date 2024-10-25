from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # AWS S3 settings
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    # App settings
    VERSION: str = "1.0"
    APP_NAME: str = "AWS S3 Proxy Service"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Server settings
    UVICORN_PORT: int = 8000
    UVICORN_HOST: str = "127.0.0.1"
    WORKERS: int = 4

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
