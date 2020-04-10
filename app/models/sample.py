from typing import Optional

from pydantic import BaseModel


class SampleInResponse(BaseModel):
    pageNumber: Optional[int] = 1
    pageSize: Optional[int] = 20
    totalCount: int
    listings: list
