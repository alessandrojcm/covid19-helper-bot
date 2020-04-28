from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute
from starlette.datastructures import FormData
from twilio.request_validator import RequestValidator

from app.core import config
from app.models import Environments

"""
    These custom classes allow us to modify and upcoming request in order
    to attach a UserIdentifier for debugging purposes
    from the Twilio Autopilot Simulator
"""


class AutopilotRequest(Request):
    async def form(self):
        if config.ENVIRONMENT != Environments.DEV:
            return await self.__handle_non_dev_env()
        return await self.__handle_dev_env()

    async def __handle_dev_env(self):
        form = await super().form()
        new_form = FormData(dict(form.items()), UserIdentifier="+15555555")
        return new_form

    async def __handle_non_dev_env(self):
        validator = RequestValidator(config.TWILIO_AUTH_TOKEN)

        params = await super().form()
        x_twilio_signature = super().headers.get("X-Twilio-Signature", "no-header")
        is_valid = validator.validate(str(super().url), params, x_twilio_signature)
        if not is_valid:
            raise HTTPException(status_code=403)
        return FormData(dict(params.items()))


class AutopilotRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = AutopilotRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
