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

    def delete(self):
        session().query(q.delete(self.ref))

        return self

    @classmethod
    def get_by_phone(cls, phone_number: str):
        result = session().query(
            q.paginate(q.match(q.index("user_by_phone_number"), phone_number))
        )
        if len(result["data"]) == 0:
            return None
        # The result is a list with the values ordered as the index defined below
        name, ref = result["data"][0]

        return UserDocument(ref=ref, name=name, phone_number=phone_number)

    @classmethod
    def delete_user_by_phone_number(cls, phone_number: str):
        user = cls.get_by_phone(phone_number)

        if not user:
            raise RuntimeError("User not found")
        result = session().query(q.delete(user.ref))
        if not result["data"]:
            raise RuntimeError("Error deleting the user, maybe does not exist?")
        return UserDocument(ref=result["ref"], **result["data"])

    @classmethod
    def _DocumentBase__initialize_indexes(cls):
        # We initialize an index in order to get users by their phone number
        session().query(
            q.create_index(
                {
                    "name": "user_by_phone_number",
                    "source": q.collection(cls._collection_name),
                    "terms": [{"field": ["data", "phone_number"]}],
                    "unique": True,
                    "values": [{"field": ["data", "name"]}, {"field": ["ref"]}],
                }
            )
        )
        session().query(
            q.create_index(
                {
                    "name": "all_users",
                    "source": q.collection(cls._collection_name),
                    "values": [
                        {"field": ["data", "name"]},
                        {"field": ["data", "phone_number"]},
                        {"field": ["ref"]},
                    ],
                }
            )
        )
