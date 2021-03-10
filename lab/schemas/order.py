from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.types import List
from typing import Optional


class OrderSchema(BaseModel):
    date: str
    samples: Optional[List[int]] = Field(None)
    element: List[int] = Field(None)
    organizationId: int
    fieldId: int
    grid: List[int]