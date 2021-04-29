from pydantic import BaseModel, Field
from pydantic.types import Json, Optional, List


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


class WorkSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    startDate: int
    endDate: int
    fieldId: int
    statusId: int
    workTypeId: int
    workSubTypeId: int
    users: Optional[List[int]] = Field(None)
    cars: Optional[List[int]] = Field(None)
    geoJson: dict

class UpdateWorkSchema(WorkSchema):
    name: Optional[str]
    description: Optional[str]
    startDate: int
    endDate: int
    statusId: int
    workTypeId: int
    workSubTypeId: int
    users: Optional[List[int]] = Field(None)
    cars: Optional[List[int]] = Field(None)
    geoJson: dict

class createWorkSchema(BaseWorkSchema):
    id: int

    class Config:
        orm_mode = True
