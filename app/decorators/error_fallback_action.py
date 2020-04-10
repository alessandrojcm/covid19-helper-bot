from functools import wraps

from fastapi import Response

from app.models import Say
from app.core import capture_message


def error_fallback_action(func):
    """
        This decorator catches unexpected errors and returns
        a fallback action for the bot to say
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, kwargs)
            return res
        except Exception as err:
            capture_message(err)
            response = Say(
                say="Ooops, looks I'm missing a screw.\nI've informed my masters, please try that again."
            )
            return Response(
                status_code=200, media_type="application/json", content=response.json()
            )

    return wrapper
