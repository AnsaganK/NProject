from . import session
from fastapi import APIRouter, Depends
from lab.models.elements import Elements
from lab.schemas.elements import ElementsSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from fastapi.security import HTTPBearer
import time

router = APIRouter()


@router.get("/")
async def get_elements():
    query = session.query(Elements).all()
    return query


@router.get("/{element_id}")
async def get_element(element_id: int):
    query = session.query(Elements).filter(Elements.id == element_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_element(element: ElementsSchema):
    query = Elements(name=element.name, code=element.code, date=element.date)
    if not query.date:
        query.date = int(time.time())
    for i in session.query(Elements).all():
        if i.name == element.name:
            return {"error": "A element with this name has already been created"}

    session.add(query)
    session.commit()

    last_id = query.id
    organization = element.dict()

    return {**organization, "id": last_id}


@router.put("/{element_id}")
async def update_element(element_id: int, element: ElementsSchema):
    query = session.query(Elements).filter(Elements.id == element_id).first()
    for i in session.query(Elements).all():
        if i.name == element.name and i.id != query.id:
            return {"error": "A element with this name has already been created"}
    if query:
        query.name = element.name
        query.code = element.code
        if element.date:
            query.date = element.date
        else:
            query.date = int(time.time())
        return {"message": "Element ({}) updated".format(query.name)}
    return {"error": "Not Found"}


@router.delete("/{element_id}")
async def delete_element(element_id:int):
    query = session.query(Elements).filter(Elements.id == element_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Element ({}) deleted".format(query.name)}
    return {"error": "Not Found"}
