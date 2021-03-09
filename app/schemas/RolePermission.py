from pydantic import BaseModel
from pydantic.types import List


class RolePermissionSchema(BaseModel):
    roles: List[int]
    permissions: List[int]


#class RolePermissionSchema(BaseModel):
#    roles: List[RoleCreateSchema]
#    permissions: List[PermissionNameSchema]