from app.models import AutopilotRequest, UserDocument


def test_greet_user_found(app, user: UserDocument):
    response = app.post(
        "/api/autopilot/greeting",
        data=AutopilotRequest(UserIdentifier=user.phone_number).json(),
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.json()
    assert response.status_code == 200


def test_greet_user_not_found(app):
    response = app.post(
        "/api/autopilot/greeting",
        data=AutopilotRequest(UserIdentifier="+15555555").json(),
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.json()
    assert response.status_code == 200


def test__bad_request_on_invalid_number(app):
    response = app.post(
        "/api/autopilot/greeting",
        data=AutopilotRequest(UserIdentifier="+12345").json(),
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
