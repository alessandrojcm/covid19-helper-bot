from app.models import DOCUMENTS
from app.core import session


def create_collections() -> None:
    """
    Helper method to create all collections defined in the models folder.
    It really does not do much, but it does not feel right to have it embedded in the cli.py
    :return: None
    """
    [Doc.create_collection(session) for Doc in DOCUMENTS]
