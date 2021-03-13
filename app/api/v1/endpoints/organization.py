from db import session
from fastapi import APIRouter, Depends, Header
from app.models.organization import Organization
from app.models.user import User
from app.schemas.organization import OrganizationSchema
from app.schemas.organizationUser import OrganizationUserSchema
from app.models.role import Role
from app.auth.auth_bearer import JWTBearer, decodeJWT
from app.auth.auth_handler import decodeJWT
from fastapi.security.http import HTTPBase
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter()


@router.get("/")
async def get_organizations():
    query = session.query(Organization).all()
    return query


@router.get("/{organization_id}")
async def get_organization(organization_id: int):# token: str = Depends(JWTBearer())):
    #user_id = decodeJWT(token)
    #print("userId: ", user_id)
    query = session.query(Organization).filter(Organization.id == organization_id).first()

    if query:
        print(query.samples)
        for i in query.users:
            for j in i.roles:
                print(j)
            print(i)

        return query
    return {"error": "Not Found"}

'''
@router.post("/")
async def create_organization(organization: OrganizationSchema):
    query = Organization(name=organization.name, bin=organization.bin, organizationId=organization.organizationId)

    for i in session.query(Organization).all():
        if i.name == organization.name:
            return {"error": "A organization with this name has already been created"}

    session.add(query)
    session.commit()

    last_id = query.id
    organization = organization.dict()

    return {**organization, "id": last_id}
'''

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
    organizationQuery = Organization(name=ou.organization.name, bin=ou.organization.bin)

    for i in session.query(Organization).all():
        if i.name == ou.organization.name:
            return {"error": "A organization with this name has already been created"}

    u = ou.userObject
    if u:
        userQuery = User(username=u.username, firstName=u.firstName, lastName=u.lastName, email=u.email, password=u.password)

        for i in session.query(User).all():
            if i.username == u.username:
                return {"error": "A user with this name has already been created"}
            if i.email == u.email:
                return {"error": "A user with this email has already been created"}

        for i in u.role:
            userId = int(i.dict()["id"])
            role = session.query(Role).filter(Role.id == userId).first()
            print(ou)
            #ou = ou.dict()
            #ou["userObject"]["role"] = []
            if role:
                #ou["userObject"]["role"].append({"id": userId})
                userQuery.roles.append(role)
        userQuery.organization.append(organizationQuery)
        session.add(userQuery)
        session.commit()

        lastId = userQuery.id

        return {**ou.dict(), "id": lastId}
    else:
        return {"error": "User objects required"}