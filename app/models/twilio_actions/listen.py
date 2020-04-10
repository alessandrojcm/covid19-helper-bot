from typing import Optional, List

from pydantic import BaseModel


class Listen(BaseModel):
    listen: bool = True
    tasks: Optional[List[str]]
