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

class RangeListSchema(BaseModel):
    name: str
    range: List[RangeSchema]

class TypeSchema(BaseModel):
    name: str
    range: List[RangeSchema]


class ElementTypeSchema(BaseModel):
    name: str
    gost: str
    description: str


class errorRange(BaseModel):
    of: float
    to: float
    value: float


class ElementsSchema(BaseModel):
    elementId: int
    colorRanges: List[RangeSchema]
    errorRanges: Optional[List[errorRange]] = Field(None)
    class Config:
        orm_mode = True

class oldElementSchema(BaseModel):
    name: str
    code: str
    date: int
    standart: bool

class ElementForTypeSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    gost: Optional[str]
    elements: List[ElementsSchema]