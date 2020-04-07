from typing import Any

from app.models.document_base import DocumentBase, q


class UserDocument(DocumentBase):
    _collection_name = "users"
    phone_number: str
    name: str

    class Config:
        extra = "allow"

    def __init__(self, **data: Any):
        super(UserDocument, self).__init__(**data)

    @classmethod
    def _DocumentBase__initialize_indexes(cls):
        from app.core.engine import session

        # We initialize an index in order to get users by their phone number
        session().query(
            q.create_index(
                {
                    "name": "users_get_by_phone",
                    "source": q.collection(cls._collection_name),
                    "terms": [{"field": ["data", "pone_number"]}],
                    "values": [{"field": ["name", "phone_number"]}, {"field": ["ref"]}],
                }
            )
        )
        session().query(
            q.create_index(
                {
                    "name": "all_users",
                    "source": q.collection(cls._collection_name),
                    "values": [{"field": ["name", "phone_number"]}, {"field": ["ref"]}],
                }
            )
        )
