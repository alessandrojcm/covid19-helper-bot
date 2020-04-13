from functools import wraps

from fastapi import Response

from app.models import Say
from app.services import capture_message


def error_fallback_action(extra_action: dict = None):
    """
        This decorator catches unexpected errors and returns
        a fallback action for the bot to say

        :param: extra_action Extra action to append to the standard fallback action (i.e a redirect) must be a dict.
    """
    response = {"actions": []}
    response.get("actions").append(
        Say(
            say="Ooops, looks I'm missing a screw.\nI've informed my masters, please try that again."
        ).dict()
    )
    if extra_action is not None:
        response.get("actions").append(extra_action)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, kwargs)
                return res
            except Exception as err:
                capture_message(err)
                return Response(
                    status_code=200, media_type="application/json", content=response
                )

        return wrapper

    return decorator
