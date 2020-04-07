from typing import Any

from app.core.engine import session
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
    def get_by_phone(cls, phone_number: str):
        result = session().query(
            q.paginate(q.match(q.index("user_by_phone_number"), phone_number))
        )
        if len(result["data"]) == 0:
            return None

        return cls.__init__(**result["data"])

    @classmethod
    def _DocumentBase__initialize_indexes(cls):
        # We initialize an index in order to get users by their phone number
        session().query(
            q.create_index(
                {
                    "name": "user_by_phone_number",
                    "source": q.collection(cls._collection_name),
                    "terms": [{"field": ["data", "phone_number"]}],
                    "values": [{"field": ["data", "name"]}],
                }
            )
        )
        session().query(
            q.create_index(
                {
                    "name": "all_users",
                    "source": q.collection(cls._collection_name),
                    "values": [],
                }
            )
        )
