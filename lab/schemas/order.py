from pydantic import BaseModel, Field, Json
from datetime import datetime
from pydantic.types import List
from typing import Optional


class OrderCellsStatusSchema(BaseModel):
    statusId: int
    miniStatusId: int


class OrderGroupSchema(BaseModel):
    name: Optional[str] = Field(None)
    date: Optional[int] = Field(None)
    userId: int
    organizationId: int

    class Config:
        orm_mode = True


class OrderSchema(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    date: Optional[int] = Field(None)
    organizationId: Optional[int] = Field(None)
    fieldId: int
    elementTypes: Optional[List[dict]]
    cellArea: Optional[float] = Field(None)
    #elements: List[int]
    grid: dict
    way: dict
    cellCount: int
    orderGroupId: Optional[int] = Field(None)
    userId: Optional[int] = Field(None)

    class Config:
        orm_mode = True
