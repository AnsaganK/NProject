from enum import Enum

from fastapi import APIRouter, Depends,Body
from sqlalchemy.orm import selectinload
from sqlalchemy import desc

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.models.cars import Car
from app.models.organization import Organization
from app.models.role import Role
from app.models.season import Season
from app.models.user import User
from app.schemas.organization import OrganizationSchema
from app.schemas.organizationUser import OrganizationUserSchema
from app.schemas.season import SeasonIdSchema
from app.schemas.user import FullUserSchema
from db import session

router = APIRouter()


@router.get("")
async def get_organizations():
    query = session.query(Organization).all()
    for i in query:
        a = i.__dict__
        a["usersCount"] = session.query(User).join(Organization).filter(Organization.id == a["id"]).count()
    return query



@router.get("/{organization_id}")
async def get_organization(organization_id: int):#, token: str = Depends(JWTBearer())):
    #user_id = decodeJWT(token)
    #print("userId: ", user_id)
    query = session.query(Organization).options(selectinload(Organization.orderGroup)).options(
        selectinload(Organization.user)).filter(Organization.id == organization_id).first()
    if query:
        a = query.__dict__
        a["usersCount"] = session.query(User).join(Organization).filter(Organization.id == a["id"]).count()
        return query
    return {"error": "Not Found"}

class RoleList(str, Enum):
    admin = "admin"
    employer = "employer"
    all = "all"

@router.get("/users/{organization_id}")
async def get_users_for_organization(organization_id: int, group: RoleList):
    # organization = session.query(Organization).filter(Organization.id == organization_id).first()
    if group == "admin":
        role = session.query(Role).filter(Role.name == "Администратор организации").first()
        users = session.query(User).filter(User.organizationId == organization_id).options(selectinload(User.roles)).filter(User.roles.any(Role.id.in_([role.id]))).all()
        return users
    if group == "employer":
        role = session.query(Role).filter(Role.name == "Сотрудник").first()
        users = session.query(User).filter(User.organizationId == organization_id).options(selectinload(User.roles)).filter(User.roles.any(Role.id.in_([role.id]))).all()
        return users
    if group == "all":
        return session.query(User).filter(User.organizationId == organization_id).options(selectinload(User.roles)).all()
    return session.query(User).filter(User.organizationId == organization_id).all()

@router.get("/selectedSeason/{organization_id}")
async def get_selected_season(organization_id: int):
    organization = session.query(Organization).filter(Organization.id == organization_id).first()
    if organization:
        return organization.selectedSeason
    return {"error": "Объект не найден"}

@router.put("/{organization_id}")
async def update_organization(organization_id: int, organization: OrganizationSchema):
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
async def delete_organization(organization_id: int):
    query = session.query(Organization).filter(Organization.id == organization_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Organization ({}) deleted".format(query.name)}
    return {"error": "Not Found"}


@router.post("/create_admin")
async def create_organization_user(ou: OrganizationUserSchema):
    organizationQuery = Organization(name=ou.organization.name, bin=ou.organization.bin)
    season = session.query(Season).order_by(desc(Season.id)).first()
    for i in session.query(Organization).all():
        if i.name == ou.organization.name:
            return {"error": "A organization with this name has already been created"}

    u = ou.userObject
    if u:
        userQuery = User(firstName=u.firstName, lastName=u.lastName, email=u.email, password=u.password)

        for i in session.query(User).all():
            if i.email == u.email:
                return {"error": "A user with this email has already been created"}
        # if u.role:
        #     # print(u.role)
        #     for i in u.role:
        #         userId = int(i)
        #         role = session.query(Role).filter(Role.id == userId).first()
        #         # print(ou)
        #         # ou = ou.dict()
        #         # ou["userObject"]["role"] = []
        #         if role:
        #             # ou["userObject"]["role"].append({"id": userId})
        #             userQuery.roles.append(role)

        organizationQuery.selectedSeason = season

        roleName = "Администратор организации"
        role = session.query(Role).filter(Role.name == roleName).first()
        userQuery.organization = organizationQuery
        if not role:
            role = Role(name=roleName)
            session.add(role)
            session.commit()
        userQuery.roles.append(role)

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

    roleName = "Администратор организации"
    role = session.query(Role).filter(Role.name == roleName).first()
    UserQuery.organization = OrganizationQuery
    if not role:
        role = Role(name=roleName)
        session.add(role)
        session.commit()
    UserQuery.roles.append(role)

    session.add(UserQuery)
    session.commit()

    last_id = UserQuery.id

    org_id = user.organizationId

    user = user.dict()

    return {**user, "organization_id": org_id, "id": last_id}

@router.post("/add_employer")
async def add_admin(user: FullUserSchema):
    UserQuery = User(firstName=user.firstName, lastName=user.lastName, email=user.email, password=user.password)
    OrganizationQuery = session.query(Organization).filter(Organization.id == user.organizationId).first()
    users = session.query(User).join(Organization).filter(Organization.id == user.organizationId).all()
    for i in users:
        if i.email == user.email:
            return {"error": "Пользователь с такой почтой уже существует"}
    if not OrganizationQuery:
        return {"error": "Организация не найдена"}

    roleName = "Сотрудник"
    role = session.query(Role).filter(Role.name == roleName).first()
    UserQuery.organization = OrganizationQuery
    if not role:
        role = Role(name=roleName)
        session.add(role)
        session.commit()
    UserQuery.roles.append(role)

    session.add(UserQuery)
    session.commit()

    last_id = UserQuery.id

    org_id = user.organizationId

    user = user.dict()

    return {**user, "organization_id": org_id, "id": last_id}

@router.get("/{organization_id}/cars")
async def get_cars_for_organization(organization_id: int):
    organization = session.query(Organization).get(organization_id)
    # cars = organization.cars
    if organization:
        cars = session.query(Car).join(Organization).options(selectinload(Car.organization)).filter(
            Organization.id == organization.id).all()
        return cars
    return {"error": "Объект не существует"}


@router.post("/{organization_id}")
async def edit_selected_season_for_organization(organization_id: int, season: SeasonIdSchema):
    organization = session.query(Organization).get(organization_id)
    season = session.query(Season).get(season.id)
    if not organization:
        return {"error": "Организация не найдена"}
    if not season:
        return {"error": "Сезон не найден"}

    organization.selectedSeason = season
    return organization.selectedSeason