from faunadb.client import FaunaClient

from .config import config

engine = FaunaClient(
    secret=config.FAUNA_SERVER_KEY,
    domain=config.FAUNA_DB_HOST,
    port=config.FAUNA_DB_PORT,
)
