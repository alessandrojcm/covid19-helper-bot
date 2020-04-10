from fastapi import APIRouter, Depends

from .hello_world import hello_world_router
from .routes.autopilot import autopilot
from ..core import config
from ..dependencies import twilio_request_validator

router = APIRouter()
router.include_router(hello_world_router)
router.include_router(
    router=autopilot,
    prefix=config.AUTOPILOT_ENDPOINT_PREFIX,
    dependencies=[Depends(twilio_request_validator)],
)
