from typing import Any

from fastapi import Header, Request, HTTPException, Form
from twilio.request_validator import RequestValidator

from app.core import config
from app.models.environments import Environments


async def twilio_request_validator(
    request: Request, x_twilio_signature: str = Header(...)
):
    if config.ENVIRONMENT == Environments.DEV:
        return request
    validator = RequestValidator(config.TWILIO_AUTH_TOKEN)

    # So I don't now why this double await is needed, but otherwise it does not work
    params = await request.form()
    is_valid = validator.validate(str(request.url), await params, x_twilio_signature)

    if not is_valid:
        raise HTTPException(status_code=403)
