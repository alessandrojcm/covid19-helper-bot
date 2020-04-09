from fastapi import FastAPI

from app.api import router


def get_application(config) -> FastAPI:
    application = FastAPI(
        title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION
    )
    application.get("")
    application.include_router(router, prefix=config.API_PREFIX)

    return application
