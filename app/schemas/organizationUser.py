from pydantic import BaseModel, Field
from .user import UserSchema
from .organization import OrganizationSchema
from typing import Optional


class OrganizationUserSchema(BaseModel):
    organization: OrganizationSchema
    userObject: Optional[UserSchema] = Field(None)


