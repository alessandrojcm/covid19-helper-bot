from faunadb.client import FaunaClient

from app.core.engine import engine, config


class FaunaClientSingleton(object):
    """
    The purpose of this singleton is to 'inject' the fauna client in all the
    classes that inherit DocumentBase, that way we avoid passing the DI dependency
    all the way up the chain.

    Granted, this is no 'true' dependency injection, but we know that this is the only
    place where the initialized engine its used.
    """

    _fauna_client: FaunaClient
    _instances = None

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self._fauna_client = engine

    def __new__(cls, *args, **kwargs):
        if not cls._instances:
            cls._instances = object.__new__(cls, *args, **kwargs)
        return cls._instances
