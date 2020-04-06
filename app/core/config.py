import logging
import sys
from os import environ

from loguru import logger
from app.core.logging import InterceptHandler
from app.models import Config, Environments

if environ.get("ENVIRONMENT", Environments.DEV):
    config = Config(_env_file=".env")
else:
    config = Config()

# logging configuration
LOGGING_LEVEL = logging.DEBUG if config.DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
