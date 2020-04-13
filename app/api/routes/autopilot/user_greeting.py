from fastapi import APIRouter, HTTPException, Form
from loguru import logger
from phonenumbers import NumberParseException

from app.decorators import error_fallback_action
from app.models import UserDocument
from app.utils import phone_to_country

user_greeting = APIRouter()


@logger.catch
@error_fallback_action
@user_greeting.post("/greeting")
def greet_user(UserIdentifier: str = Form(...)):
    try:
        country = phone_to_country(UserIdentifier)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid phone number")

    user = UserDocument.get_by_phone(UserIdentifier)

    # TODO: Had to remove the Pydantic models because there are some quirks rendering correct json data
    # need to find a workaround around this
    if user is not None:
        return {
            "actions": [
                {"remember": {"name": user.name, "country": user.country}},
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
