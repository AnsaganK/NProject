from . import session
from app.models.role import Role
from app.schemas.role import RoleCreateSchema
from app.schemas.RolePermission import RolePermissionSchema
from app.models.RolePermission import RolesPermissions

import databases
from app.models import DATABASE_URL

database = databases.Database(DATABASE_URL)


class CRUD_ROLE:
    def __init__(self):
        pass


    async def get_roles(self):
        query = session.query(Role).all()
        return query


    async def get_role(role_id: int):
        query = session.query(Role).filter(Role.id == role_id).first()
        if query:
            return query
        return {"error": "Not Found"}


    async def create_roles(role: RoleCreateSchema):
        query = Role(name=role.name)

        for i in session.query(Role).all():
            if i.name == role.name:
                return {"error": "A role with this name has already been created"}

        session.add(query)
        session.commit()

        last_id = query.id
        permission = role.dict()

        return {**permission, "id": last_id}


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


    async def delete_roles(role_id: int):
        query = session.query(Role).filter(Role.id == role_id).first()
        if query:
            session.delete(query)
            session.commit()
            return {"message": "Role ({}) deleted".format(query.name)}
        return {"error": "Not Found"}


    async def get_RP(self):
        query = RolesPermissions.select()
        queries = await database.fetch_all(query)
        for i in queries:
            print(i)
        return queries


    async def create_role_permission(rp: RolePermissionSchema):
        for i in rp.roles:
            role = session.query(Role).filter(Role.id == int(i)).first()
            if role:
                for j in rp.permissions:
                    print(role.permissions)
                    role.permissions.add(j)
                    session.add(role)
                    session.commit()
            else:
                return {"error": "Not Found Roles"}
        return {**rp.dict()}
