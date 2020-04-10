from traceback import format_exception_only

from loguru import logger
from sentry_sdk import init, capture_message as log_to_sentry

from app.core import config
from app.models.environments import Environments


def init_sentry():
    if config.ENVIRONMENT != Environments.DEV:
        # Don't initialize in dev
        init(dsn=config.SENTRY_DSN)


def capture_message(msg: Exception):
    if config.ENVIRONMENT != Environments.DEV:
        # We're not on dev we log to sentry, else just log to loguru
        log_to_sentry(format_exception_only(Exception, msg))
    logger.error(format_exception_only(Exception, msg))
