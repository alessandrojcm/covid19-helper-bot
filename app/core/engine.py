from faunadb.client import FaunaClient

_session = None


def session():
    from .config import config
    from app.models.environments import Environments

    global _session
    if _session is None and config.ENVIRONMENT == Environments.DEV:
        # We only need the Fauna Host if we are running from other server that's not the faunadb.com official server
        _session = FaunaClient(
            secret=config.FAUNA_SERVER_KEY.get_secret_value(),
            domain=config.FAUNA_DB_URL.host,
            port=config.FAUNA_DB_URL.port,
            scheme=config.FAUNA_DB_URL.scheme,
        )
    elif _session is None:
        _session = FaunaClient(secret=config.FAUNA_SERVER_KEY.get_secret_value())
    return _session
