from pydantic import BaseModel, Field
from pydantic.types import Optional

class BaseWorkSubType(BaseModel):
    name: str
    description: Optional[str] = Field(None)
    default: bool = Field(default=True)
    groupId: int


class workSubTypeSchema(BaseWorkSubType):
    pass

class createWorkSubTypeSchema(BaseWorkSubType):
    id: int

    class Config:
        orm_mode = True
