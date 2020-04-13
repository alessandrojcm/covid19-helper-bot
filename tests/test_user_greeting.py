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


def test_bad_request_on_invalid_number(app):
    response = app.post(
        "/api/autopilot/greeting",
        data={"UserIdentifier": "+12345"},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Twilio-Signature": "",
        },
    )
    assert response.status_code == 400
