from pydantic import BaseModel, Field
from pydantic.types import Optional

class TillageSchema(BaseModel):
    name: str
    description: Optional[str] = Field(None)

class CreateTillageSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None)

    class Config:
        orm_mode = True