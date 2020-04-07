from typing import Any

from app.models.document_base import DocumentBase, q, FaunaClient


class UserDocument(DocumentBase):
    _collection_name = "users"
    phone_number: str
    name: str

    def __init__(self, **data: Any):
        super().__init__(**data)

    @classmethod
    def _DocumentBase__initialize_indexes(cls, session: FaunaClient):
        # We initialize an index in order to get users by their phone number
        session.query(
            q.create_index(
                {
                    "name": "get_by_phone",
                    "source": q.collection(cls._collection_name),
                    "values": [{"field": ["data", "phone_number"]}],
                }
            )
        )
