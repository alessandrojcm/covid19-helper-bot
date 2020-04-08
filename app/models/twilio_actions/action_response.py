from pydantic import BaseModel


class ActionResponse(BaseModel):
    actions: list
