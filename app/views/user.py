from app.schemas.user import UserLoginSchema
from db import session
from app.models.user import User


def check_user(data: UserLoginSchema):
    for user in session.query(User).all():
        if user.username == data.username and user.password == data.password:
            return user.id
    return False
