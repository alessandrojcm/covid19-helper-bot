from fastapi import APIRouter

from .hello_world import hello_world_router
from .routes.autopilot import autopilot
from ..core import config

router = APIRouter()
router.include_router(hello_world_router)
router.include_router(router=autopilot, prefix=config.AUTOPILOT_ENDPOINT_PREFIX)
