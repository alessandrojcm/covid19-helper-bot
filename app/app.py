from fastapi import FastAPI

from app.api import router
from app.core.environments import Environments


def get_application(config) -> FastAPI:
    application = FastAPI(
        title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION
    )
    application.get("")
    application.include_router(router, prefix=config.API_PREFIX)

    if config.ENVIRONMENT == Environments.DEV:
        return application
    return sentry_handler(config)(application)


def sentry_handler(config):
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(dsn=config.SENTRY_DSN)
    return SentryAsgiMiddleware
