from abc import abstractmethod
from datetime import datetime
from typing import Any

from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.errors import BadRequest
from loguru import logger
from pydantic import BaseModel

from app.models.singleton import Singleton


class DocumentBase(BaseModel, Singleton):
    _collection_name: str
    _fauna_client: FaunaClient
    _instance = None
    ts: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, engine: FaunaClient, **data: Any):
        super().__init__(**data)
        self._fauna_client = engine

    @classmethod
    def create_collection(cls, session: FaunaClient):
        cls.__initialize_collection(session)
        cls.__initialize_indexes(session)

    @classmethod
    @logger.catch
    def __initialize_collection(cls, session):
        logger.info(
            "Checking if collection {c} exists...".format(c=cls._collection_name)
        )
        try:
            session.query(q.get(q.collection(cls._collection_name)))
            logger.info("{c} exists, skipping creation.".format(c=cls._collection_name))
        except BadRequest:
            logger.info(
                "{c} does not exist, creating...".format(c=cls._collection_name)
            )
            session.query(q.create_collection({"name": cls._collection_name}))

    @classmethod
    @abstractmethod
    def __initialize_indexes(self, session: FaunaClient):
        """
        This method must be overridden in order to create indexes to query the db.
        """
        pass

    @logger.catch
    def save(self):
        """
        Saves the document in the collection,
        the attributes are serialized utilizing Pydantic's dict method, which
        traverses trough the child class attributes
        :return: An instance of the newly saved object.
        """
        attributes = self.dict(exclude={"ts"})
        logger.debug(
            "Saving object for collection {c} with attributes {attr}".format(
                c=self._collection_name, attr=attributes
            )
        )
        result = self._fauna_client.query(
            q.create(
                q.collection(self._collection_name),
                {
                    **attributes,
                    "create_at": datetime.now(),
                    "updated_at": datetime.now(),
                },
            )
        )
        logger.debug("Object saved with id {ts}".format(ts=result.ts))

        return self.__init__(**result)
