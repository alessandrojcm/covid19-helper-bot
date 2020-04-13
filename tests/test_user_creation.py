from app.models import UserDocument


def test_user_creation(config):
    user = UserDocument(phone_number="+15555555", name="Joe", country="Venezuela")
    new_user = user.save()

    assert new_user.ts is not None

    new_user.delete()
