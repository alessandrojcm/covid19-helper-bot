import json
from os import environ

from app.models import UserDocument


def test_greet_user_found(app, user: UserDocument, action_schema):
    response = app.post(
        "/api/autopilot/greeting",
        data={"UserIdentifier": user.phone_number},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Twilio-Signature": "",
        },
    )
    assert action_schema(response.json()) is None
    assert response.status_code == 200


def test_greet_user_not_found(app, action_schema):
    response = app.post(
        "/api/autopilot/greeting",
        data={"UserIdentifier": "+15555555"},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Twilio-Signature": "",
        },
    )
    assert action_schema(response.json()) is None
    assert response.status_code == 200


# fixme: this test it's broken due to the custom router for dev mode
def test_bad_request_on_invalid_number(app):
    environ["ENVIRONMENT"] = "stating"
    response = app.post(
        "/api/autopilot/greeting",
        data={"UserIdentifier": "+12345"},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Twilio-Signature": "",
        },
    )
    assert response.status_code == 400


def test_can_have_name_yes(app, action_schema):
    response = app.post(
        "api/autopilot/can-have-name",
        data={
            "UserIdentifier": "+12345",
            "Memory": json.dumps(
                {
                    "twilio": {
                        "collected_data": {
                            "ask-for-name": {
                                "answers": {"can_have_name": {"answer": "Yes"}}
                            }
                        }
                    }
                }
            ),
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Twilio-Signature": "",
        },
    )

    assert response.status_code == 200
    assert action_schema(response.json()) is None


def test_can_have_name_no(app, action_schema):
    response = app.post(
        "api/autopilot/can-have-name",
        data={
            "UserIdentifier": "+12345",
            "Memory": json.dumps(
                {
                    "twilio": {
                        "collected_data": {
                            "ask-for-name": {
                                "answers": {"can_have_name": {"answer": "No"}}
                            }
                        }
                    }
                }
            ),
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Twilio-Signature": "",
        },
    )

    assert response.status_code == 200
    assert action_schema(response.json()) is None


def test_store_user(app, action_schema):
    response = app.post(
        "api/autopilot/store-user",
        data={
            "UserIdentifier": "+15555555",
            "Memory": json.dumps(
                {
                    "twilio": {
                        "collected_data": {
                            "collect-name": {
                                "answers": {"first_name": {"answer": "Alessandro"}}
                            }
                        }
                    }
                }
            ),
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Twilio-Signature": "",
        },
    )

    assert response.status_code == 200
    assert action_schema(response.json()) is None
