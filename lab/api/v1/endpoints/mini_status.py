from db import session
from fastapi import APIRouter
from lab.models.mini_status import MiniStatus
from lab.schemas.mini_status import MiniStatusSchema


router = APIRouter()


@router.get("")
async def get_mini_status():
    query = session.query(MiniStatus).all()
    return query


@router.get("/{mini_status_id}")
async def get_mini_status(mini_status_id: int):
    query = session.query(MiniStatus).filter(MiniStatus.id == mini_status_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("")
async def create_mini_status(mini_status: MiniStatusSchema):
    query = MiniStatus(name=mini_status.name)

    for i in session.query(MiniStatus).all():
        if i.name == mini_status.name:
            return {"error": "A mini status with this name has already been created"}

    session.add(query)
    session.commit()

    last_id = query.id
    mini_status = mini_status.dict()

    return {**mini_status, "id": last_id}


@router.put("/{status_id}")
async def update_status(mini_status_id: int, mini_status: MiniStatusSchema):
    query = session.query(MiniStatus).filter(MiniStatus.id == mini_status_id).first()
    for i in session.query(MiniStatus).all():
        if i.name == query.name and i.id != mini_status_id:
            return {"error": "A MiniStatus with this name has already been created"}
    if query:
        query.name = mini_status.name
        return {"message": "MiniStatus ({}) updated".format(query.name)}
    return {"error": "Not Found"}


@router.delete("/{mini_status_id}")
async def delete_order(mini_status_id: int):
    query = session.query(MiniStatus).filter(MiniStatus.id == mini_status_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "MiniStatus ({}) deleted".format(query.name)}
    return {"error": "Not Found"}
