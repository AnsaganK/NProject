from pydantic import BaseModel


class StatusSchema(BaseModel):
    name: str