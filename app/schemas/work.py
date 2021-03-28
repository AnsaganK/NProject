from pydantic import BaseModel
from pydantic.types import Json, Optional


class BaseWorkSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    startDate: int
    endDate: int
    fieldId: int
    statusId: int
    workTypeId: int
    workSubTypeId: int
    geoJson: dict


class WorkSchema(BaseWorkSchema):
    pass


class createWorkSchema(BaseWorkSchema):
    id: int
    class Config:
        orm_mode = True
