from typing import Optional, List

from pydantic import BaseModel


class Listen(BaseModel):
    listen: Optional[bool]
    tasks: Optional[List[str]]
