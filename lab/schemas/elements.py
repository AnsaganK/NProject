from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from typing import Optional, List


class NewColorSchema(BaseModel):
    name: Optional[str] = Field(None)

    class Config:
        orm_mode = True

class ColorSchema(BaseModel):
    name: Optional[str] = Field(None)
    code: str

    class Config:
        orm_mode = True

class RangeSchema(BaseModel):
    name: str
    of: float
    to: float
    color: int


class TypeSchema(BaseModel):
    name: str
    range: List[RangeSchema]


class ElementTypeSchema(BaseModel):
    name: str
    gost: str
    description: str



class ElementsSchema(BaseModel):
    name: str
    code: str
    date: Optional[int] = Field(None)
    standard: bool = Field(default=False)
    types: List[TypeSchema]

    class Config:
        orm_mode = True


class ElementForTypeSchema(BaseModel):
    elements: List[ElementsSchema]