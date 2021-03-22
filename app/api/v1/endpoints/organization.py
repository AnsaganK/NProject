from db import session
from fastapi import APIRouter, Depends, Header
from app.models.organization import Organization
from app.models.user import User
from app.schemas.user import FullUserSchema
from app.schemas.organization import OrganizationSchema
from app.schemas.organizationUser import OrganizationUserSchema
from app.models.role import Role
from app.auth.auth_bearer import JWTBearer, decodeJWT
from app.auth.auth_handler import decodeJWT
from fastapi.security.http import HTTPBase
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/")
async def get_organizations():
    query = session.query(Organization).all()
    for i in query:
        a = i.__dict__
        a["usersCount"] = session.query(User).join(Organization).filter(Organization.id == a["id"]).count()
    return query


@router.get("/{organization_id}")
async def get_organization(organization_id: int, token: str = Depends(JWTBearer())):
    user_id = decodeJWT(token)
    print("userId: ", user_id)
    query = session.query(Organization).options(selectinload(Organization.orderGroup)).options(selectinload(Organization.user)).filter(Organization.id == organization_id).first()
    if query:
        a = query.__dict__
        a["usersCount"] = session.query(User).join(Organization).filter(Organization.id == a["id"]).count()
        return query
    return {"error": "Not Found"}


@router.put("/{organization_id}")
async def update_organization(organization_id:int, organization: OrganizationSchema):
    query = session.query(Organization).filter(Organization.id == organization_id).first()
    for i in session.query(Organization).all():
        if i.name == organization.name and i.id != query.id:
            return {"error": "A organization with this name has already been created"}
    if query:
        query.name = organization.name
        query.bin = organization.bin
        return {"message": "Organization ({}) updated".format(query.name)}
    return {"error": "Not Found"}


@router.delete("/{organization_id}")
async def delete_organization(organization_id:int):
    query = session.query(Organization).filter(Organization.id == organization_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Organization ({}) deleted".format(query.name)}
    return {"error": "Not Found"}

@router.post("/create_admin")
async def create_organization_user(ou: OrganizationUserSchema):
    print(ou)
    organizationQuery = Organization(name=ou.organization.name, bin=ou.organization.bin)

    for i in session.query(Organization).all():
        if i.name == ou.organization.name:
            return {"error": "A organization with this name has already been created"}

    u = ou.userObject
    if u:
        userQuery = User(firstName=u.firstName, lastName=u.lastName, email=u.email, password=u.password)

        for i in session.query(User).all():
            if i.email == u.email:
                return {"error": "A user with this email has already been created"}
        if u.role:
            #print(u.role)
            for i in u.role:
                userId = int(i)
                role = session.query(Role).filter(Role.id == userId).first()
                #print(ou)
                #ou = ou.dict()
                #ou["userObject"]["role"] = []
                if role:
                    #ou["userObject"]["role"].append({"id": userId})
                    userQuery.roles.append(role)
        
        userQuery.organization = organizationQuery
        session.add(userQuery)
        session.commit()

        lastId = userQuery.id

        return {**ou.dict(), "id": lastId}
    else:
        return {"error": "User objects required"}

@router.post("/add_admin")
async def add_admin(user: FullUserSchema):
    UserQuery = User(firstName=user.firstName, lastName=user.lastName, email=user.email, password=user.password)
    OrganizationQuery = session.query(Organization).filter(Organization.id == user.organizationId).first()
    users = session.query(User).join(Organization).filter(Organization.id == user.organizationId).all()
    for i in users:
        if i.email == user.email:
            return {"error": "Пользователь с такой почтой уже существует"}
    if not OrganizationQuery:
        return {"error": "Организация не найдена"}
    UserQuery.organization = OrganizationQuery

    session.add(UserQuery)
    session.commit()

    last_id = UserQuery.id

    org_id = user.organizationId

    user = user.dict()

    return {**user,"organization_id": org_id, "id": last_id}