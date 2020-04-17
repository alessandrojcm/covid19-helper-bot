from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.datastructures import FormData

from app.core import config
from app.models import Environments

"""
    These custom classes allow us to modify and upcoming request in order
    to attach a UserIdentifier for debugging purposes
    from the Twilio Autopilot Simulator
"""


class UserIdentifierRequest(Request):
    async def form(self):
        if config.ENVIRONMENT != Environments.DEV:
            return super().form()
        form = await super().form()
        new_form = FormData(form.items(), UserIdentifier="+15555555")
        return new_form


class UserIdentifierRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = UserIdentifierRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
