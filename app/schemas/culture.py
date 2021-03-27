from pydantic import BaseModel, Field
from pydantic.types import Optional


class CultureSchema(BaseModel):
    name: str
    default: bool = Field(default=True)
    shortName: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    fillColor: str


class CreateCultureSchema(BaseModel):
    id: int
    name: str
    default: bool = Field(default=True)
    shortName: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    fillColor: str

    class Config:
        orm_mode = True