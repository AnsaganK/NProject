from pydantic import BaseModel

class CarBase(BaseModel):
    name: str
    number: str
    organizationId: int
    terminalId: str

class CarSchema(CarBase):
    pass

class CarCreateSchema(CarBase):
    id: int

    class Config:
        orm_mode = True