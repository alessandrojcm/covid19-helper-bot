from os import environ

import pytest
from starlette.testclient import TestClient

from app import get_application
from app.core.config import config as app_config
from app.models.environments import Environments

environ["ENVIRONMENT"] = Environments.DEV


@pytest.fixture(scope="function")
def config():
    environ["DEBUG"] = "True"
    environ["TESTING"] = "True"
    environ["ENVIRONMENT"] = "dev"

    return app_config


@pytest.fixture(scope="function")
def app(config):
    return TestClient(get_application(config))


@pytest.fixture(scope="function")
def user():
    from app.models import UserDocument

    user = UserDocument(
        phone_number="+581234566", name="Juan", country="Venezuela"
    ).save()

    yield user

    user.delete()
