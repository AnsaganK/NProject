from pydantic import BaseModel, Field
from pydantic.types import Optional

class IrrigationTypeSchema(BaseModel):
    name: str
    description: Optional[str] = Field(None)


class CreateIrrigationTypeSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True