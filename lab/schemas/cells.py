from pydantic import BaseModel


class OrderCellsResultSchema(BaseModel):
    elementId: int
    result: float
