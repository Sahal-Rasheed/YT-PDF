import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

MAX_BYTES = 50 * 1024 * 1024  # 50MB
BACKUP_COUNT = 5


def get_rotating_file_handler(filename: str) -> RotatingFileHandler:
    """
    Create a rotating file handler for the given filename
    """
    log_file = LOGS_DIR / filename
    handler = RotatingFileHandler(
        log_file, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    return handler


def configure_logging():
    """
    Logging Configuration for Application.
    """

    # Base Config
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            get_rotating_file_handler("app.log"),
        ],
    )

    # Uvicorn logger
    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.propagate = False
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_logger.addHandler(get_rotating_file_handler("uvicorn.log"))

    # FastAPI logger
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(logging.INFO)

    # SQLAlchemy logger
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.propagate = False
    sqlalchemy_logger.setLevel(logging.WARN)
    sqlalchemy_logger.addHandler(logging.StreamHandler())
    sqlalchemy_logger.addHandler(get_rotating_file_handler("sqlalchemy.log"))

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
