from fastapi import FastAPI

from app.api.routes.api import router as api_router
from app.core import config
from app.core.events import create_start_app_handler
from app.scripts import cli


def get_application() -> FastAPI:
    application = FastAPI(
        title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION
    )
    application.include_router(api_router, prefix=config.API_PREFIX)

    application.add_event_handler("startup", create_start_app_handler(application))

    return application


app = get_application()

# To be run in dev mode
if __name__ == "__main__":
    cli()
