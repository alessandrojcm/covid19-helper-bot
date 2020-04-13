import json
from os import environ
from functools import partial

import pytest
from starlette.testclient import TestClient
import jsonschema

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


@pytest.fixture(scope="session")
def action_schema():
    """
        Load schema to validate Autopilot Actions against
    """
    schema = {}
    with open("./actions_schema.json") as file:
        schema = json.loads(file.read())

    def validator(instance):
        return jsonschema.validate(instance, schema)

    yield validator
