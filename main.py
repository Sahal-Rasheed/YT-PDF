import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logging import configure_logging
from api import api_router as api_router_v1


configure_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    docs_url=f"{settings.API_V1_STR}/docs" if settings.DEBUG else None,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
    redoc_url=None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    logger.info("YT-PDF API is running...")
    return {"message": "YT-PDF API is running..."}


app.include_router(api_router_v1, prefix=settings.API_V1_STR)
