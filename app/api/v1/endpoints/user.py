from db import session
from fastapi import APIRouter

from sqlalchemy.orm import selectinload
from app.schemas.user import UserSchema
from app.schemas.UserRole import UserRoleSchema
from app.models.user import User
from app.models.role import Role

router = APIRouter()


@router.post("")
async def create_user(userSchema: UserSchema):
    users = session.query(User).all()
    for i in users:
        if i.email == userSchema.email:
            return {"error": "A user with this email already been created"}
    user = User(firstName=userSchema.firstName, lastName=userSchema.lastName, password=userSchema.password, email=userSchema.email)
    for i in userSchema.role:
        role = session.query(Role).filter(Role.id == i).first()
        if role:
            user.roles.append(role)

    session.add(user)
    session.commit()
    last_id = user.id

    return {**userSchema.dict(), "id": last_id}

@router.get("")
def get_all():
    query = session.query(User).options(selectinload(User.roles)).all()
    return query


@router.get("/{user_id}")
async def user_detail(user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        return {"user_id": user.id, "organization": user.organization, "user_name": user.username}
    return {"error": "There is no user with this ID"}


@router.put("/{user_id}")
async def user_update(user_id: int, user: UserSchema):
    query = session.query(User).filter(User.id == user_id).first()
    if user:
        for i in session.query(User).all():
            if i.email == user.email and i.id != user_id:
                return {"error": "A user with this email already been created"}

        query.firstName = user.firstName
        query.lastName = user.lastName
        query.email = user.email
        query.password = user.password
        session.add(query)
        session.commit()
        return {"user_id": query.id, "user_name": query.name}

    return {"error": "There is no user with this ID"}


@router.delete("/{user_id}")
async def user_delete(user_id: int):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        return {"message": "user ({}) delete".format(user.name)}
    else:
        return {"error": "There is no user with this ID"}


@router.post("/UserRole")
async def create_user_role(ur: UserRoleSchema):
    dic = {}
    dic["users"] = []
    dic["roles"] = []
    for i in ur.users:
        user = session.query(User).filter(User.id == int(i)).first()
        if user:
            dic["users"].append(i)
            for j in ur.roles:
                print(ur.roles)
                role = session.query(Role).filter(Role.id == int(j)).first()
                if role:
                    dic["roles"].append(j)
                    print(i)
                    print("  ", j)
                    user.roles.append(role)
                    session.add(user)
                    session.commit()
    return dic
