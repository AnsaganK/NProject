from pydantic import BaseModel
from enum import Enum

class StatusName(str, Enum):
    planned = "planned"
    selection = "selection"
    preparation = "preparation"
    laboratory = "laboratory"
    agrohym = "agrohym"


status_dict = [
    {"name": StatusName.planned, "code": StatusName.planned},
    {"name": StatusName.selection, "code": StatusName.selection},
    {"name": StatusName.preparation, "code": StatusName.preparation},
    {"name": StatusName.laboratory, "code": StatusName.laboratory},
    {"name": StatusName.agrohym, "code": StatusName.agrohym},
]

class StatusSchema(BaseModel):
    name: str


class StatusIdSchema(BaseModel):
    statusName: StatusName