from abc import abstractmethod
from datetime import datetime
from typing import Any, Optional, Union

import pytz
from faunadb import query as q
from faunadb.errors import BadRequest
from faunadb.objects import Ref, FaunaTime
from loguru import logger
from pydantic import BaseModel

from app.core.engine import session


class DocumentBase(BaseModel):
    _collection_name: str
    ref: Optional[Ref]
    ts: Optional[str]
    created_at: Union[datetime, FaunaTime] = datetime.now(pytz.timezone("UTC"))
    updated_at: Union[datetime, FaunaTime] = datetime.now(pytz.timezone("UTC"))

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    def __init__(self, **data: Any):
        super().__init__(**data)

    @classmethod
    def create_collection(cls):
        cls.__initialize_collection()
        cls.__initialize_indexes()

    @classmethod
    @logger.catch
    def __initialize_collection(cls):
        from app.core.engine import session

        logger.info(
            "Checking if collection {c} exists...".format(c=cls._collection_name)
        )
        try:
            session().query(q.get(q.collection(cls._collection_name)))
            logger.info("{c} exists, skipping creation.".format(c=cls._collection_name))
        except BadRequest:
            logger.info(
                "{c} does not exist, creating...".format(c=cls._collection_name)
            )
            session().query(q.create_collection({"name": cls._collection_name}))

    @classmethod
    @abstractmethod
    def __initialize_indexes(cls):
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
        attributes = self.dict()
        logger.debug(
            "Saving object for collection {c} with attributes {attr}".format(
                c=self._collection_name, attr=attributes
            )
        )
        result = session().query(
            q.create(q.collection(self._collection_name), {"data": attributes},)
        )
        logger.debug("Object saved with id {ts}".format(ts=result["ts"]))

        return self.__init__(ref=result["ref"], ts=result["ts"], **result["data"])
