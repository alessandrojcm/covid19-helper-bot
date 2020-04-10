from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from twilio.request_validator import RequestValidator

from app.core import config


class TwilioRequestValidator(BaseHTTPMiddleware):
    """
        Starlette Middleware to validate that request come from Twilio
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        validator = RequestValidator(config.TWILIO_AUTH_TOKEN)

        is_valid = validator.validate(
            request.url, request.form(), request.headers.get("X-TWILIO-SIGNATURE", "")
        )

        if not is_valid:
            raise HTTPException(status_code=403)
        return await call_next(request)
