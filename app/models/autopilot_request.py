from fastapi import Form
from pydantic import BaseModel, Extra


class AutopilotRequest(BaseModel):
    user_identifier: str

    def __init__(self, UserIdentifier: str = Form(...)) -> None:
        super().__init__(**{"user_identifier": UserIdentifier})

    class Config:
        extra = Extra.allow
