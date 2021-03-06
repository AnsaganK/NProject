from db import session
from fastapi import APIRouter
from app.schemas.role import RoleCreateSchema
from app.schemas.RolePermission import RolePermissionSchema
from app.models.role import Role, RolesPermissions
from app.models.permission import Permission

import databases
from app.models import DATABASE_URL

database = databases.Database(DATABASE_URL)

router = APIRouter()


@router.get("")
async def get_roles():
    query = session.query(Role).all()
    for i in query:
        pass
    return query


@router.post("")
async def create_roles(role: RoleCreateSchema):
    query = Role(name=role.name, title=role.title)

    for i in session.query(Role).all():
        if i.name == role.name:
            return {"error": "A role with this name has already been created"}

    session.add(query)
    session.commit()

    last_id = query.id
    permission = role.dict()

    return {**permission, "id": last_id}

@router.get("/{role_id}")
async def get_roles(role_id: int):
    query = session.query(Role).filter(Role.id == role_id).first()
    if query:
        return query
    return {"error": "Not Found"}





@router.put("/{role_id}")
async def update_role(role_id: int, role: RoleCreateSchema):
    query = session.query(Role).filter(Role.id == role_id).first()

    if query:
        for i in session.query(Role).all():
            if i.name == role.name and i.id != role_id:
                return {"error": "A role with this name has already been created"}

        query.name = role.name
        session.add(query)
        session.commit()
        return {"message": "Role ({}) updated".format(query.name)}
    return {"error": "Not Found"}


@router.delete("/{role_id}")
async def delete_roles(role_id: int):
    query = session.query(Role).filter(Role.id == role_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Role ({}) deleted".format(query.name)}
    return {"error": "Not Found"}

