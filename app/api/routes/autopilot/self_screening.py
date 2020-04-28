import json
from typing import List, Dict
from itertools import chain

import faunadb.errors
from loguru import logger
from requests.exceptions import BaseHTTPError
from fastapi import APIRouter, Form

from app.core import config
from app.custom_routers import AutopilotRoute
from app.models import UserDocument
from app.services import capture_message
from app.services.endless_medical_api import EndlessMedicalAPI
from app.utils import features_mapping, reponse_mappings, outcomes_mapping

self_screening = APIRouter()
self_screening.route_class = AutopilotRoute
endless_medical_api = EndlessMedicalAPI(config)


@self_screening.post("/self-screening/start")
def self_screening_start(UserIdentifier: str = Form(...), Memory: str = Form(...)):
    memory = json.loads(Memory)
    twilio = memory.pop("twilio")

    start_screening = twilio["collected_data"]["accepts-test"]["answers"][
        "start-screening"
    ]["answer"]

    if start_screening == "Yes" and not UserDocument.get_by_phone(UserIdentifier):
        return {
            "actions": {
                "actions": [
                    {
                        "say": "Sorry, I cannot continue until you give me your name \U00012639"
                    },
                    {"redirect": "task://can-have-name"},
                ]
            }
        }
    elif start_screening == "Yes":
        return {
            "actions": [
                {"say": "Alright, let's start"},
                {"redirect": "task://self-screening-lives-in-area"},
            ]
        }
    return {
        "actions": [
            {"say": "Cool! No problem, let's get back to the menu"},
            {"redirect": "task://menu-description"},
        ]
    }


@self_screening.post("/self-screening/lives-in-area")
def self_screening_start(UserIdentifier: str = Form(...), Memory: str = Form(...)):
    memory = json.loads(Memory)
    twilio = memory.pop("twilio")

    start_screening = twilio["collected_data"]["q1"]["answers"]["lives-in-area"][
        "answer"
    ]

    if start_screening == "No":
        return {
            "actions": [
                {
                    "say": """Great! Then you probably do't have anything to worry about!
                                  Feel free to run the test again if you want"""
                },
                {"redirect": "task://menu-description"},
            ]
        }
    try:
        endless_medical_session_id = endless_medical_api.get_session_token()
        if not endless_medical_api.accept_tos(endless_medical_session_id):
            raise BaseHTTPError("Error accepting Endless Medical TOS")
        user = UserDocument.get_by_phone(UserIdentifier)
        user.endless_medical_token = endless_medical_session_id
        logger.debug(
            "Adding {feature} with value {value}".format(
                feature=features_mapping.get("lives-in-area"), value=5
            )
        )
        # 5 is the endless medical api value for "lives in a covid 19 affected area" we assume so because
        # to get into this step the user must have answered yes to this question in a previous step
        # the options was not added to the mapping since overlaps with the "severe" answer mapping
        endless_medical_api.add_feature(
            endless_medical_session_id, features_mapping.get("lives-in-area"), 5
        )

        user.update()

        return {"actions": [{"redirect": "task://self-screening-q-rest"}]}
    except faunadb.errors.BadRequest as err:
        capture_message(err)
        return {"actions": [{"redirect": "task://fallback"}]}
    except BaseHTTPError as err:
        capture_message(err)
        return {"actions": [{"redirect": "task://fallback"}]}


@self_screening.post("/self-screening/analyze-answers")
def analyze_answers(UserIdentifier: str = Form(...)):
    # We don't need to access collect since arriving here means
    # all answers have been added to the Endless Medical Session
    session_id = UserDocument.get_by_phone(UserIdentifier).endless_medical_token

    def reset_session_id_token():
        user = UserDocument.get_by_phone(UserIdentifier)
        user.endless_medical_token = None
        user.update()

    try:
        fix_response: List[Dict[str, str]] = [
            {
                "say": """
                            Please bear in mind that this tool is merely informative.
                            If, after all, you don't feel ill there should not be any cause for alarm
                        """
            },
            {"redirect": "task://menu-description"},
        ]

        outcomes: List[Dict[str, str]] = endless_medical_api.analyse(session_id)[
            "Diseases"
        ]
        logger.debug(outcomes)
        # Parsing the diseases, the API returns a confidence from 0.0 to 1.0 for every predicted disease
        # if COVID-19 has >= 50 % we recommend calling the doctor; else we check if any other diseases has at least
        # 50 % chance, if so, COVID-19 it's discarded but we recommend calling the doctor anyway

        # Check if COVID-19 passes threshold
        if check_outcomes(outcomes, outcomes_mapping.get("covid-19")):
            return {
                "actions": list(
                    chain(
                        [
                            {
                                "say": "You should seek medical attention as soon as possible"
                            }
                        ],
                        fix_response,
                    )
                )
            }

        # COVID-19 did not pass threshold, check now if any other outcome does
        if check_outcomes(outcomes):
            return {
                "actions": list(
                    chain(
                        [
                            {
                                "say": "You probably do not have COVID-19, but, according to your symptoms, you should seek medical attention anyways"
                            }
                        ],
                        fix_response,
                    )
                )
            }

        return {
            "actions": [
                {
                    "say": "Great news! You don not have anything to worry about 🥳\U0001f973"
                },
                {"redirect": "task://menu-description"},
            ]
        }
    except BaseHTTPError as err:
        capture_message(err)

        return {
            "actions": [
                {
                    "say": "Sorry, our super AI doctor had a problem analysing the results; please try again."
                },
                {"redirect": "task://menu-description"},
            ]
        }
    finally:
        reset_session_id_token()


@self_screening.post("/self-screening/{feature}")
def add_feature(
    feature: str, UserIdentifier: str = Form(...), ValidateFieldAnswer: str = Form(...)
):
    """
        This endpoint gets called when the user answers a question from the self screening collect,
        the path param must match the symptoms on the feature_mappings and the answer must match
        the ones in the response_mapping. If successful, adds the feature to the Endless Medical
        current session.
    """
    session_id = UserDocument.get_by_phone(UserIdentifier).endless_medical_token
    try:
        logger.debug(
            "Adding {feature} with {value}".format(
                feature=features_mapping[feature],
                value=reponse_mappings[ValidateFieldAnswer.lower()],
            )
        )
        res = endless_medical_api.add_feature(
            session_id,
            features_mapping[feature],
            reponse_mappings[ValidateFieldAnswer.lower()],
        )
        logger.debug(res)
        if not res:
            return {"valid": False}
        return {"valid": True}
    except BaseHTTPError as err:
        capture_message(err)
        return {"valid": False}
    except KeyError as err:
        capture_message(err)
        return {"valid": False}


# The following is horrible, but the API response mapping is not... Ideal
# Helper method to check if an outcome (or any outcome) passes threshold
def check_outcomes(outcomes: List[Dict[str, str]], name: str = None) -> bool:
    for outcome in outcomes:
        disease_name = list(outcome.keys())[0]
        confidence = float(list(outcome.values())[0])

        if name and disease_name == name and confidence >= config.OUTCOME_THRESHOLD:
            return True
        elif not name and confidence >= config.OUTCOME_THRESHOLD:
            return True
    return False
