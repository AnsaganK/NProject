from pydantic import BaseModel, Field, Json
from datetime import datetime
from pydantic.types import List
from typing import Optional



class OrderSchema(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    date: int
    organizationId: int
    fieldId: int
    elements: List[int]
    grid: dict
    cellCount: int