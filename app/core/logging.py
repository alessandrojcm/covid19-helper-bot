import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Loguru interceptor to route stout to loguru
    """

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        logger_opt = logger.opt(depth=7, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())
