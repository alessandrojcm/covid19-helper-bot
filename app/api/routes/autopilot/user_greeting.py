import json

from fastapi import APIRouter, HTTPException, Form
from loguru import logger

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


@logger.catch
@error_fallback_action
@user_greeting.post("/can-have-name")
async def can_have_name(Memory: str = Form(...)):
    memory = json.loads(Memory)

    answer = memory["twilio"]["collected_data"]["ask-for-name"]["answers"][
        "can_have_name"
    ]["answer"]
    if answer == "Yes":
        return {"actions": [{"redirect": "task://store-user"}]}
    return {
        "actions": [
            {
                "say": """Ok no biggie! Just keep in mind that I won't be able to offer you all my
                        capabilities unless I have your name.\n If you change you"""
            },
            {"redirect": "task://menu-description"},
        ]
    }


@logger.catch
@error_fallback_action(extra_action={"redirect": "task://store-user"})
@user_greeting.post("/store-user")
def store_user(UserIdentifier: str = Form(...), Memory: str = Form(...)):
    memory = json.loads(Memory)
    name = memory["twilio"]["collected_data"]["collect-name"]["answers"]["first_name"][
        "answer"
    ]

    try:
        country = phone_to_country(UserIdentifier)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    new_user = UserDocument(
        name=name, phone_number=UserIdentifier, country=country
    ).save()

    return {
        "actions": [
            {"remember": {"name": new_user.name, "country": new_user.country}},
            {
                "say": "Great! {name} I got that, let's begin!".format(
                    name=new_user.name
                )
            },
            {"redirect": "task://menu-description"},
        ]
    }
