from typing import Union

from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.api import router
from app.services import init_sentry
from app.core.environments import Environments


def get_application(config) -> Union[FastAPI, SentryAsgiMiddleware]:
    application = FastAPI(
        title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION
    )
    application.get("")
    application.include_router(router, prefix=config.API_PREFIX)
    init_middlewares()

    if config.ENVIRONMENT == Environments.DEV:
        return application
    return SentryAsgiMiddleware(application)


def init_middlewares():
    init_sentry()
