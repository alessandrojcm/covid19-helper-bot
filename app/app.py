from fastapi import FastAPI

from app.api.routes.api import router as api_router


def get_application(config) -> FastAPI:
    application = FastAPI(
        title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION
    )
    application.include_router(api_router, prefix=config.API_PREFIX)

    return application
