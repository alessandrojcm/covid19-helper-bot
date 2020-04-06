import logging
import sys

from loguru import logger
from starlette.config import environ
from app.core.logging import InterceptHandler
from app.models import Config

if environ.get("ENVIRONMENT", "dev"):
    config = Config(_env_file=".env")
else:
    config = Config()

# logging configuration
LOGGING_LEVEL = logging.DEBUG if config.DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
