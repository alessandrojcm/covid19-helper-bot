from pydantic import BaseModel, Extra


class AutopilotRequest(BaseModel):
    UserIdentifier: str

    class Config:
        extra = Extra.allow
