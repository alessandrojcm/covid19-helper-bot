from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute
from starlette.datastructures import FormData
from twilio.request_validator import RequestValidator

from app.core import config
from app.models import Environments


class AutopilotRequest(Request):
    """
    This class serves two purposes. First one, know that Starlette (framework on which Fastapi is built upon)
    is an ASGI framework. That means that parts of the request (like the body) are async. So, if we await
    those streams in a middleware they will be consumed and will not be available to the final route.

    For that, this class consumes the steam (in this case the form) does what it needs to do with the data,
    and the creates a new FormData object to pass to the final route.
    """

    async def form(self):
        if config.ENVIRONMENT != Environments.DEV:
            return await self.__handle_non_dev_env()
        return await self.__handle_dev_env()

    async def __handle_dev_env(self):
        """
        Here we just inject a fake number for testing, this so we can test from
        the Twilio Autopilot Simulator through an SSH tunnel.
        """
        form = await super().form()
        new_form = FormData(dict(form.items()), UserIdentifier=config.FAKE_NUMBER)
        return new_form

    async def __handle_non_dev_env(self):
        """
        In production or staging, validate that the request comes from Twilio
        """
        validator = RequestValidator(config.TWILIO_AUTH_TOKEN)

        params = await super().form()
        x_twilio_signature = super().headers.get("X-Twilio-Signature", "no-header")
        is_valid = validator.validate(str(super().url), params, x_twilio_signature)
        if not is_valid:
            raise HTTPException(status_code=403)
        return FormData(dict(params.items()))


class AutopilotRoute(APIRoute):
    """
    Custom route to route requests through our AutopilotRequest object
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = AutopilotRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
