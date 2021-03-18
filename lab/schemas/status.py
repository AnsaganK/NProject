from pydantic import BaseModel
from enum import Enum

class StatusName(str, Enum):
    planned = "planned"
    selection = "selection"
    notSelection = "notSelection"
    preparation = "preparation"
    notPreparation = "notPreparation"
    laboratory = "laboratory"
    notLaboratory = "notLaboratory"
    agrohym = "agrohym"


status_dict = [
    {"name": StatusName.planned, "code": StatusName.planned},
    {"name": StatusName.selection, "code": StatusName.selection},
    {"name": StatusName.notSelection, "code": StatusName.notSelection},
    {"name": StatusName.preparation, "code": StatusName.preparation},
    {"name": StatusName.notPreparation, "code": StatusName.notPreparation},
    {"name": StatusName.laboratory, "code": StatusName.laboratory},
    {"name": StatusName.notLaboratory, "code": StatusName.notLaboratory},
    {"name": StatusName.agrohym, "code": StatusName.agrohym},
]

class StatusSchema(BaseModel):
    name: str


class StatusIdSchema(BaseModel):
    status: StatusName