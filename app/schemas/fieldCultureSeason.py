from pydantic import BaseModel
from pydantic.types import Optional
from app.schemas.field import FieldSchema

class FieldCultureSeasonSchema(BaseModel):
    fieldId: int
    cultureId: int
    seasonId: int
    irrigationTypeId: int
    tillageId: int
    sort: Optional[str] = None

    sowingDate: int
    cleaningDate: int

    prolificness: int
    harvest: int


class CreateFieldCultureSeasonSchema(BaseModel):
    id: int
    fieldId: int
    cultureId: int
    seasonId: int
    irrigationTypeId: int
    tillageId: int
    sort: Optional[str] = None

    sowingDate: int
    cleaningDate: int

    prolificness: int
    harvest: int

    class Config:
        orm_mode = True
