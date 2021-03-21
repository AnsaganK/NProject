from pydantic import BaseModel


class MiniStatusSchema(BaseModel):
    name: str
    color: str