from pydantic import BaseModel


class elementTypeSchema(BaseModel):
    name: str
    description: str
