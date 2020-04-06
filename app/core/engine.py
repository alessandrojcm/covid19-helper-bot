from faunadb.client import FaunaClient

from .config import config

session = FaunaClient(
    secret=config.FAUNA_SERVER_KEY.get_secret_value(),
    domain=config.FAUNA_DB_URL.host,
    port=config.FAUNA_DB_URL.port,
    scheme=config.FAUNA_DB_URL.scheme,
)
