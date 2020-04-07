from faunadb.client import FaunaClient

_session = None


def session():
    from .config import config

    global _session
    if _session is None:
        _session = FaunaClient(
            secret=config.FAUNA_SERVER_KEY.get_secret_value(),
            domain=config.FAUNA_DB_URL.host,
            port=config.FAUNA_DB_URL.port,
            scheme=config.FAUNA_DB_URL.scheme,
        )
    return _session
