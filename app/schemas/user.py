from pydantic import BaseModel, Field, EmailStr
from .role import RoleForUserSchema
from pydantic.types import List, Optional

class FullUserSchema1(BaseModel):
    firstName: str = Field(...)
    lastName: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: List[RoleForUserSchema] = Field(None)

class FullUserSchema(BaseModel):
    firstName: str = Field(...)
    lastName: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    organizationId: int = Field(None)
    role: List[int] = Field(None)

class UserSchema(BaseModel):
    firstName: str = Field(...)
    lastName: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: Optional[List[RoleForUserSchema]] = Field(None)


class UserLoginSchema(BaseModel):
    id: int = Field(None)
    email: EmailStr = Field(...)
    password: str = Field(...)
