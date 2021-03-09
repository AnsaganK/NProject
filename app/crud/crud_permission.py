from . import session
from app.models.permission import Permission
from app.schemas.permission import PermissionSchema

class CRUD_PERMISSION:
    def __init__(self):
        pass


    async def get_permissions(self):
        query = session.query(Permission).all()
        return query


    async def get_permission(permission_id: int):
        query = session.query(Permission).filter(Permission.id == permission_id).first()
        if query:
            return query
        return {"error": "Not Found"}


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


    async def delete_permission(permission_id: int):
        query = session.query(Permission).filter(Permission.id == permission_id).first()
        if query:
            session.delete(query)
            session.commit()
            return {"message": "Permission ({}) deleted".format(query.name)}
        return {"error": "Not Found"}


