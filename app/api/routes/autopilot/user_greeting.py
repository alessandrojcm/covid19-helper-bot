from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from phonenumbers import NumberParseException

from app.decorators import error_fallback_action
from app.models import AutopilotRequest, UserDocument
from app.utils import phone_to_country

user_greeting = APIRouter()


@logger.catch
@user_greeting.post("/greeting")
@error_fallback_action
def greet_user(data: AutopilotRequest = Depends()):
    request = data["data"]
    try:
        country = phone_to_country(request.user_identifier)
    except NumberParseException:
        raise HTTPException(status_code=400, detail="Invalid phone number")

    user = UserDocument.get_by_phone(request.user_identifier)

    # TODO: Had to remove the Pydantic models because there are some quirks rendering correct json data
    # need to find a workaround around this
    if user is not None:
        return {
            "actions": [
                {
                    "say": "Hi there! {name}, what can I do for you today?".format(
                        name=user.name
                    )
                },
                {"listen": {"tasks": ["menu-description"]}},
            ]
        }
    return {
        "actions": [
            {
                "say": "Hello there! Looks like you're writing from {country}, great to meet you! Can I have your name?".format(
                    country=country
                )
            },
            {"listen": {"tasks": ["menu-description", "store-user"]}},
        ]
    }
