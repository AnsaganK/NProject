from pydantic import BaseModel


class PermissionSchema(BaseModel):
    name: str
    code: str


class PermissionNameSchema(BaseModel):
    name: str
