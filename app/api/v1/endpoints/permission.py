from . import session
from fastapi import APIRouter
from app.models.permission import Permission
from app.schemas.permission import PermissionSchema

router = APIRouter()


@router.get("/")
async def get_permissions():
    query = session.query(Permission).all()
    return query


@router.get("/{permission_id}")
async def get_permission(permission_id: int):
    query = session.query(Permission).filter(Permission.id == permission_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_permission(permission: PermissionSchema):
    query = Permission(name=permission.name, code=permission.code)
    for i in session.query(Permission).all():
        if i.name == permission.name:
            return {"error": "A permission with this name has already been created"}
        if i.code == permission.code:
            return {"error": "A permission with this code has already been created"}

    session.add(query)
    session.commit()

    last_id = query.id
    permission = permission.dict()

    return {**permission, "id": last_id}


@router.put("/{permission_id}")
async def update_permission(permission_id: int, permission: PermissionSchema):
    query = session.query(Permission).filter(Permission.id == permission_id).first()

    if query:
        for i in session.query(Permission).all():
            if i.name == permission.name and i.id != permission_id:
                return {"error": "A permission with this name has already been created"}
            if i.code == permission.code and i.id != permission_id:
                return {"error": "A permission with this code has already been created"}

        query.name = permission.name
        query.code = permission.code
        session.add(query)
        session.commit()
        return {"message": "Permission ({}) updated".format(query.name)}
    return {"error": "Not Found"}


@router.delete("/{permission_id}")
async def delete_roles(permission_id: int):
    query = session.query(Permission).filter(Permission.id == permission_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Permission ({}) deleted".format(query.name)}
    return {"error": "Not Found"}