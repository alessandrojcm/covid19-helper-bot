from fastapi import APIRouter, HTTPException
from loguru import logger

from app.models import AutopilotRequest, UserDocument, Say, Listen
from app.models.twilio_actions import ActionResponse
from app.utils import phone_to_country

user_greeting = APIRouter()


@logger.catch
@user_greeting.post("/greeting")
def greet_user(request: AutopilotRequest):
    try:
        country = phone_to_country(request.UserIdentifier)
    except ValueError:
        raise HTTPException(status_code=400)

    user = UserDocument.get_by_phone(request.UserIdentifier)

    if user is not None:
        return ActionResponse(
            actions=[
                Say(
                    say="Hi there! {name}, what can I do for you today?".format(
                        name=user.name
                    )
                ),
                Listen(tasks=["menu-description"]),
            ]
        )

    return ActionResponse(
        actions=[
            Say(
                say="Hello there! Looks like you're writing from {country}, great to meet you! Can I have your name?".format(
                    country=country
                )
            ),
            Listen(tasks=["store-user", "menu-description"]),
        ]
    )
