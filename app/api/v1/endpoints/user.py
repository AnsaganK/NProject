from app.models.organization import Organization
from db import session
from fastapi import APIRouter

from sqlalchemy.orm import selectinload
from app.schemas.user import UserSchema, userForRolesSchema, allFullUserSchema
from app.schemas.UserRole import UserRoleSchema
from app.models.user import User
from app.models.role import Role

router = APIRouter()


@router.post("")
async def create_user(userSchema: userForRolesSchema):
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
    user = session.query(User).options(selectinload(User.organization)).filter(User.id == user_id).first()
    if user:
        return user.__dict__
    return {"error": "There is no user with this ID"}

@router.get("/roles/{role_id}")
async def get_users_for_role(role_id: int):
    role = session.query(Role).filter(Role.id == role_id).first()
    users = role.users
    return users

@router.put("/{user_id}")
async def user_update(user_id: int, user: allFullUserSchema):
    query = session.query(User).filter(User.id == user_id).options(selectinload(User.roles)).first()
    organization = session.query(Organization).filter(Organization.id == user.organizationId).first()
    if not organization:
        return {"error": "Организация не найдена"}
    if user:
        for i in session.query(User).all():
            if i.email == user.email and i.id != user_id:
                return {"error": "A user with this email already been created"}

        query.firstName = user.firstName
        query.lastName = user.lastName
        query.email = user.email
        query.password = user.password
        query.organization = organization

        query.roles = []

        for i in user.roles:
            role = session.query(Role).filter(Role.id == i).first()
            query.roles.append(role)

        session.add(query)
        session.commit()
        return {**(user.__dict__)}

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
