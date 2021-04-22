from pydantic import BaseModel
from pydantic.types import List


class BaseOrderPointsSchema(BaseModel):
    orderId: int
    orderGroupId: int
    dateCreate: int


class OrderPointsSchema(BaseOrderPointsSchema):
    latitude: float
    longitude: float
    pass


class CreateOrderPointsSchema(BaseOrderPointsSchema):
    id: int
