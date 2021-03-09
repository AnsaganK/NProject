from pydantic import BaseModel
from app.schemas.user import UserSchema
from app.schemas.organization import OrganizationSchema, OrganizationGetId
from pydantic.types import List
from lab.schemas.elements import ElementsSchema
from datetime import datetime
from typing import Optional
from pydantic import Field


class SamplesSchema(BaseModel):
    client: List[int]
    amount: int
    elements: Optional[List[int]] = Field(None)
    date: Optional[int] = Field(None)
