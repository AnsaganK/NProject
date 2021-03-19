from pydantic import BaseModel


class TypesForFieldSchema(BaseModel):
    name: str
    key: str
