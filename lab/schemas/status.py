from pydantic import BaseModel


class StatusSchema(BaseModel):
    name: str


class StatusIdSchema(BaseModel):
    statusId: int