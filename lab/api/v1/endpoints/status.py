from db import session
from fastapi import APIRouter
from lab.schemas.status import StatusSchema
from lab.models.status import Status
from app.models.role import Role


router = APIRouter()


@router.get("")
async def get_status():
    query = session.query(Status).all()
    return query

@router.get("/{status_id}")
async def get_status(status_id: int):
    query = session.query(Status).filter(Status.id == status_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_status(status: StatusSchema):
    query = Status(name=status.name, color=status.color)

    for i in session.query(Status).all():
        if i.name == status.name:
            return {"error": "A status with this name has already been created"}

    role = session.query(Role).filter(Role.id == status.roleEdit).first()
    if role:
        query.role_edit = role

    role = session.query(Role).filter(Role.id == status.roleSelect).first()
    if role:
        query.role_selection = role

    session.add(query)
    session.commit()

    last_id = query.id
    status = status.dict()

    return {**status, "id": last_id}

@router.delete("/{status_id}")
async def delete_order(status_id: int):
    query = session.query(Status).filter(Status.id == status_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Status ({}) deleted".format(query.name)}
    return {"error": "Not Found"}

'''
@router.put("/{status_id}")
async def update_status(status_id: int, status: StatusSchema):
    query = session.query(Status).filter(Status.id == status_id).first()
    if query:
        query.name = status.name
        return {"message": "Status ({}) updated".format(query.name)}
    return {"error": "Not Found"}


@router.delete("/{status_id}")
async def delete_order(status_id: int):
    query = session.query(Status).filter(Status.id == status_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Status ({}) deleted".format(query.name)}
    return {"error": "Not Found"}
'''
