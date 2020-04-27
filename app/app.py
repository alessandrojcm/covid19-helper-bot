from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.api import router
from app.middlewares import MIDDLEWARES
from app.models.environments import Environments
from app.services import init_sentry
from app.error_handlers import error_fallback_action


def get_application(config) -> Union[FastAPI, SentryAsgiMiddleware]:
    application = FastAPI(
        title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION
    )
    application.exception_handler(StarletteHTTPException)(error_fallback_action)
    application.include_router(router, prefix=config.API_PREFIX)
    application.get("/")(lambda: RedirectResponse(config.API_PREFIX))

    if config.ENVIRONMENT == Environments.DEV:
        return application
    init_middlewares(application)
    return SentryAsgiMiddleware(application)


def init_middlewares(application):
    [application.add_middleware(middleware) for middleware in MIDDLEWARES]
    init_sentry()
