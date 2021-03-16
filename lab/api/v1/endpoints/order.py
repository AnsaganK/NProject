from db import session
from fastapi import APIRouter, Depends, Query, Response, status
from lab.models.order import Order
from app.models.organization import Organization
from lab.models.elements import Elements
from lab.models.cells import Cells
from lab.models.status import Status
from app.models.field import Field
from lab.schemas.order import OrderSchema
import time

router = APIRouter()


@router.get("/")
async def get_order():
    query = session.query(Order).all()
    return query


@router.get("/{order_id}")
async def get_order(element_id: int):
    query = session.query(Order).filter(Order.id == element_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_order(order: OrderSchema):
    query = Order(name=order.name, description=order.description, date=order.date, grid=order.grid, cellCount=order.cellCount, way=order.way)
    if not query.date:
        query.date = int(time.time())
    organization = session.query(Organization).filter(Organization.id == order.organizationId).first()
    if not organization:
        return {"error": "Not Found Organization"}
    query.organization = organization
    field = session.query(Field).filter(Field.id == order.fieldId).first()
    if not field:
        return {"error": "Not Found Field"}
    query.field = field
    for i in query.elements:
        element = session.query(Elements).filter(Elements.id == i).first()
        query.elements.append(element)
    status = session.query(Status).filter(Status.id == 1).first()
    for i in range(1, order.cellCount+1):
        cell = Cells(code=i)
        if status:
            cell.status = status
        #cell.order = query
        query.cells.append(cell)
    session.add(query)
    session.commit()

    #for i in range(1,query.cellCount+1):
    last_id = query.id
    organization = order.dict()

    return {**organization, "id": last_id}


@router.put("/{order_id}")
async def update_order(order_id: int, order: OrderSchema):
    query = session.query(Order).filter(Order.id == order_id).first()
    if query:
        query.name = order.name
        query.description = order.description
        if order.date:
            query.date = order.date
        else:
            query.date = int(time.time())
        query.grid = order.grid
        query.cellCount = order.cellCount
        return {"message": "Order ({}) updated".format(query.name)}
    return {"error": "Not Found"}


@router.delete("/{order_id}")
async def delete_order(order_id: int):
    query = session.query(Order).filter(Order.id == order_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Order ({}) deleted".format(query.name)}
    return {"error": "Not Found"}