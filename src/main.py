import uvicorn
from fastapi import FastAPI

from api.routes import router
from config.settings import get_settings
from core.logging import get_logger

logger = get_logger()
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

app.include_router(router)

if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    uvicorn.run(
        "main:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        workers=settings.WORKERS,
        reload=settings.ENVIRONMENT == "development"
    )
