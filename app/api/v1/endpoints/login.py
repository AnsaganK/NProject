from fastapi import APIRouter, Depends
from fastapi import Body

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserSchema, UserLoginSchema
from db import session
from app.views.user import check_user
from app.auth.auth_handler import decodeJWT

router = APIRouter()

@router.get("/me")
async def auth_me(token: str = Depends(JWTBearer())):
    decode = decodeJWT(token)
    print(decode)
    if "id" in decode:
        return decode
    else:
        return {"error": "Вы не авторизованы"}


@router.post("/user/signup")
async def create_user(user: UserSchema = Body(...)):
    query = User(firstName=user.firstName,
                 lastName=user.lastName,
                 email=user.email,
                 password=user.password)


    for i in session.query(User).all():
        if i.email == user.email:
            return {"error": "A user with this email has already been created"}

    for i in user.role:
        r = session.query(Role).filter(Role.id == int(i.id)).first()
        if r:
            query.roles.append(r)

    session.add(query)
    session.commit()
    last_id = query.id
    return {**user.dict(), "id": last_id}


@router.post("/user/login")
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(check_user(user))
    return {
        "error": "Неправильный логин или пароль"
    }

