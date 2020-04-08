from fastapi import APIRouter

from .routes.autopilot import autopilot
from ..core import config

router = APIRouter()
router.include_router(router=autopilot, prefix="/" + config.AUTOPILOT_ENDPOINT_PREFIX)
