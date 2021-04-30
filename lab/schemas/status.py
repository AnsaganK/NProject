from pydantic import BaseModel, Field
from enum import Enum
from pydantic.types import Optional, List

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
    color: Optional[str] = Field(None)
    roleEdit: Optional[int] = Field(None)
    roleSelect: Optional[int] = Field(None)


class StatusIdSchema(BaseModel):
    status: StatusName