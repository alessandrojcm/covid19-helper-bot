import json

from fastapi import APIRouter, HTTPException, Form
from loguru import logger

from app.custom_router import AutopilotRoute
from app.models import UserDocument
from app.utils import phone_to_country

user_greeting = APIRouter()
user_greeting.route_class = AutopilotRoute


@logger.catch
@user_greeting.post("/greeting")
def greet_user(UserIdentifier: str = Form(...)):
    """
    User greet endpoint
    :param: UserIdentifier: user's phone number from Twilio
    """

    # Check the country from the phone number
    try:
        country = phone_to_country(UserIdentifier)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid phone number")

    user = UserDocument.get_by_phone(UserIdentifier)

    # Greeting the user since already exists
    if user is not None:
        return {
            "actions": [
                {"remember": {"name": user.name, "country": user.country}},
                {"say": "Hi there {name}!".format(name=user.name)},
                {"redirect": "task://menu-description"},
            ]
        }
    return {
        "actions": [
            {
                "say": "Hello there! Looks like you're writing from {country}, great to meet you!".format(
                    country=country
                )
            },
            {"redirect": "task://can-have-name"},
        ]
    }


@logger.catch
@user_greeting.post("/can-have-name")
async def can_have_name(Memory: str = Form(...)):
    """
    Asks the user if he/she wants to give us their name
    :param: Memory: JSON Stringified object from Twilio
    """
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
                        capabilities unless I have your name"""
            },
            {"redirect": "task://menu-description"},
        ]
    }


@logger.catch
@user_greeting.post("/store-user")
def store_user(UserIdentifier: str = Form(...), Memory: str = Form(...)):
    """
    Stores a user in the database, fields stored are: country, name and phone number
    :param: UserIdentifier: Phone number from Twilio
    :param: Memory: JSON Stringified object from Twilio
    """
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
