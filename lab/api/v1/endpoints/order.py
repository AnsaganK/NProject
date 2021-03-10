from . import session
from fastapi import APIRouter, Depends, Query, Response, status
from lab.models.order import Order
from lab.schemas.order import OrderSchema
import time

router = APIRouter()


@router.get("/")
async def get_orders(*, main: bool = Query(False)):
    query = session.query(Order).all()
    return query


@router.get("/{element_id}")
async def get_element(element_id: int):
    query = session.query(Order).filter(Elements.id == element_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_element(element: ElementsSchema):
    query = Elements(name=element.name, code=element.code, standard=element.standard, date=element.date)
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
        query.standard = element.standard
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
