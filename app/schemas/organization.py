from pydantic import BaseModel
from pydantic.types import List

class OrganizationSchema(BaseModel):
    name: str
    bin: str

class OrganizationGetId(BaseModel):
    id: int


class OrganizationUserSchema(OrganizationSchema):
    user: List[dict]
    selectedSeasonId: int