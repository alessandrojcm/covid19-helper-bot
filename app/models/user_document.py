from app.models import DocumentBase, q


class UserDocument(DocumentBase):
    _collection_name = "users"
    phone_number: str
    name: str

    def __initialize_indexes(self):
        # We initialize an index in order to get users by their phone number
        self._fauna_client.query(
            q.create_index(
                {
                    "name": "get_by_phone",
                    "source": q.collection(self._collection_name),
                    "values": [{"field": ["data", "phone_number"]}],
                }
            )
        )
