from db import session
from fastapi import APIRouter, Depends, Query, Response, status
from lab.models.order import Order, OrderCells
from app.models.organization import Organization
from lab.models.elements import Elements
from lab.models.cells import Cells
from app.models.field import Field
from lab.schemas.order import OrderSchema
from lab.schemas.status import StatusName, StatusIdSchema
import time
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/")
async def get_order():
    query = session.query(Order).all()
    return query

@router.post("/status/")
async def get_cells_for_order(status: StatusIdSchema):
    print(status)
    print(OrderCells.status)
    #orderCells = session.query(OrderCells).filter(OrderCells.status == status).all()
    #orderCells = session.query(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.status == status).all()
    #cells = session.query(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.status == status).all()
    orderCells = session.query(OrderCells).join(Order).filter(OrderCells.status == status.status).subquery()
    orders = session.query(Order).join(orderCells).filter(OrderCells.orderId == Order.id).all()
    print(orders)
    return orders


@router.get("/{order_id}")
async def get_order(order_id: int):
    query = session.query(Order).filter(Order.id == order_id).first()
    if query:
        a = query.cells
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_order(order: OrderSchema):
    query = Order(name=order.name, description=order.description, date=order.date, grid=order.grid, cellCount=order.cellCount, way=order.way)
    if not query.date:
        query.date = int(time.time())*1000
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
    status = "planned"
    for i in range(1, order.cellCount+1):
        cell = Cells(code=i)
        date = int(time.time())*1000
        if status:
            orderCells = OrderCells(status=status, order=query, cell=cell, date=date)
        else:
            orderCells = OrderCells(order=query, cell=cell, date=date)
        session.add(orderCells)
    session.add(query)
    session.commit()

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
            query.date = int(time.time())*1000
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