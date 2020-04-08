from os import environ

import pytest
from starlette.testclient import TestClient

from app import get_application
from app.core.environments import Environments
from app.core.config import config

environ["ENVIRONMENT"] = Environments.DEV


@pytest.fixture(scope="function")
def app():
    return TestClient(get_application(config))


@pytest.fixture(scope="function")
def user():
    from app.models import UserDocument

    user = UserDocument(phone_number="+581234567", name="Juan")
    user.save()

    yield user

    user.delete()
