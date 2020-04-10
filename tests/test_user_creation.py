from os import environ

import pytest

from app.models import UserDocument


@pytest.fixture(scope="module")
def config():
    environ["DEBUG"] = True
    environ["TESTING"] = True


def test_user_creation():
    user = UserDocument(phone_number="5555555", name="Joe")
    new_user = user.save()

    assert new_user.ts is not None
