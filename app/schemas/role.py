from pydantic import BaseModel
from pydantic.types import List
from app.schemas.permission import PermissionSchema


class RoleCreateSchema(BaseModel):
    name: str


class RoleSchema(BaseModel):
    name: str
    permissions: List[PermissionSchema]


class RoleForUserSchema(BaseModel):
    id: int
