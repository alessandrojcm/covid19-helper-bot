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
        if request.url.path.find(config.AUTOPILOT_ENDPOINT_PREFIX) == -1:
            # Make exception for docs or /
            return await call_next(request)

        validator = RequestValidator(config.TWILIO_AUTH_TOKEN)

        is_valid = validator.validate(
            str(request.url),
            await request.form(),
            request.headers.get("X-TWILIO-SIGNATURE", ""),
        )

        if not is_valid:
            return Response(status_code=403)
        return await call_next(request)
