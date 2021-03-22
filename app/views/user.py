from app.schemas.user import UserLoginSchema
from db import session
from app.models.user import User
import json

def check_user(data: UserLoginSchema):
    for user in session.query(User).all():
        if user.email == data.email and user.password == data.password:

            roles = []
            for i in user.roles:
                dic = {}
                dic["id"] = i.id
                dic["name"] = i.name
                roles.append(dic)
            return {"id": user.id, "email": user.email, "organization": user.organization, "roles": roles}
    return False
