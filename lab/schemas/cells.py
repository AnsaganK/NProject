from pydantic import BaseModel
from pydantic.types import List

class ResultList(BaseModel):
    elementId: int
    value: float


class OrderCellsResultSchema(BaseModel):
    results: List[ResultList]


class EditCellsArrayData(BaseModel):
    cellCode: int
    statusId: int
    miniStatusId: int

class EditCellsArray(BaseModel):
    cells: List[EditCellsArrayData]