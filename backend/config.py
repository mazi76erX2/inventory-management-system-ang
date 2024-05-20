""" Application configuration """

import os
import logging

from dotenv import load_dotenv

from fastapi.logger import logger as fastapi_logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db/inventory-management-system",
)

LOGGING_FORMAT = "%(levelname)s: %(name)s: %(message)s"


def configure_logging():
    """Configures logging for the application"""
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
    fastapi_logger.setLevel(logging.INFO)


configure_logging()


# SECURITY WARNING: don't run with debug turned on in production!
def str2bool(arg: int | str) -> bool:
    """
    Converts string to Boolean for .env file
    """
    return str(arg).lower() in ("1", "true")


DEBUG = str2bool(os.getenv("DEBUG", "false"))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

NUM_ITEMS = int(os.getenv("NUM_ITEMS", 50))
NUM_CATEGORIES = int(os.getenv("NUM_CATEGORIES", 10))
NUM_SUPPLIERS = int(os.getenv("NUM_SUPPLIERS", 10))
