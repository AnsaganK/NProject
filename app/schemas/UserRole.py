from pydantic import BaseModel
from pydantic.types import List


class UserRoleSchema(BaseModel):
    users: List[int]
    roles: List[int]
