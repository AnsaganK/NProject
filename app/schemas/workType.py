from pydantic import BaseModel, Field
from pydantic.types import Optional


class BaseWorkType(BaseModel):
    name: str
    description: Optional[str] = Field(None)
    default: bool = Field(default=True)


class workTypeSchema(BaseWorkType):
    pass

class createWorkTypeSchema(BaseWorkType):
    id: int

    class Config:
        orm_mode = True