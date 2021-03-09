from pydantic import BaseModel, Field, EmailStr
from .role import RoleForUserSchema
from pydantic.types import List

class FullUserSchema(BaseModel):
    username: str = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    organizationId: int = Field(None)
    role: List[RoleForUserSchema] = Field(None)

class UserSchema(BaseModel):
    username: str = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: List[RoleForUserSchema] = Field(None)


class UserLoginSchema(BaseModel):
    id: int = Field(None)
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "username",
                "password": "12345"
            }
        }
