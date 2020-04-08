from pydantic import BaseModel


class Say(BaseModel):
    say: str
