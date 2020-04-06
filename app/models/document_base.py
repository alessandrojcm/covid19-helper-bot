from abc import abstractmethod
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from faunadb import query as q
from loguru import logger

from app.models.fauna_client_singleton import FaunaClientSingleton


class DocumentBase(BaseModel, FaunaClientSingleton):
    _collection_name: str

    ts: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.__initialize_collection()
        self.__initialize_indexes()

    @logger.catch
    def __initialize_collection(self):
        logger.info(
            "Checking if collection {c} exists...".format(c=self._collection_name)
        )
        if self._fauna_client.query(q.get(self._collection_name)):
            logger.info(
                "{c} exists, skipping creation.".format(c=self._collection_name)
            )
            return
        logger.info("{c} does not exist, creating...".format(c=self._collection_name))
        self._fauna_client.query(q.create_collection({"name": self._collection_name}))

    @property
    @abstractmethod
    def __collection__name__(self) -> str:
        pass

    @__collection__name__.setter
    @abstractmethod
    def __collection__name__(self, collection_name: str):
        self._collection_name = collection_name

    @abstractmethod
    def __initialize_indexes(self):
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
