from pydantic import BaseModel

class SeasonSchema(BaseModel):
    name: str
    of: int
    to: int


class CreateSeasonSchema(BaseModel):
    id: int
    name: str
    of: int
    to: int

    class Config:
        orm_mode = True


class SeasonIdSchema(BaseModel):
    id: int