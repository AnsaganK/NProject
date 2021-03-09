from pydantic import BaseModel


class OrganizationSchema(BaseModel):
    name: str
    bin: str

class OrganizationGetId(BaseModel):
    id: int
