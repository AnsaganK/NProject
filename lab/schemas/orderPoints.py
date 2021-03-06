from pydantic import BaseModel
from pydantic.types import List


class BaseOrderPointsSchema(BaseModel):
    orderId: int
    orderGroupId: int
    points: List[dict]
    dateCreate: int


class OrderPointsSchema(BaseOrderPointsSchema):
    pass


class CreateOrderPointsSchema(BaseOrderPointsSchema):
    id: int
