from pydantic import BaseModel
from app.schemas.user import UserSchema
from app.schemas.organization import OrganizationSchema, OrganizationGetId
from pydantic.types import List
from lab.schemas.elements import ElementsSchema
from datetime import datetime
from typing import Optional
from pydantic import Field
from enum import Enum


class Types(Enum):
    standard = "standard"
    custom = "custom"

class SamplesSchema(BaseModel):
    client: List[int]
    amount: int = Field(..., ge=1)
    standard: bool = Field(default=False)
    elements: Optional[List[int]] = Field(None)
    date: Optional[int] = Field(None)
