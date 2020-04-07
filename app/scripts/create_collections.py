from app.models import DOCUMENTS


def create_collections() -> None:
    """
    Helper method to create all collections defined in the models folder.
    It really does not do much, but it does not feel right to have it embedded in the cli.py
    :return: None
    """
    [Doc.create_collection() for Doc in DOCUMENTS]
