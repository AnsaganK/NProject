from db import session
from fastapi import APIRouter, Depends, Query, Response, status
from lab.models.order import Order, OrderCells, OrderGroup
from app.models.organization import Organization
from lab.models.elements import Elements
from lab.models.cells import Cells
from app.models.field import Field
from lab.schemas.order import OrderSchema
from lab.schemas.status import StatusName, StatusIdSchema
import time
from sqlalchemy.orm import selectinload, load_only

router = APIRouter()




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

@router.get("/groups")
async def get_order_group():
    query = session.query(OrderGroup).all()
    for i in query:
        a = i.__dict__
        zero = 0
        for j in session.query(Order).session.query(Order).join(OrderGroup).filter(OrderGroup.id == a["id"]):
            c = len(j.cells)
            zero+=c

        a["cellsCount"] = zero
        a["orderCount"] = session.query(Order).join(OrderGroup).filter(OrderGroup.id == a["id"]).count()
    return query


@router.get("/{order_id}")
async def get_order(order_id: int):
    query = session.query(Order).filter(Order.id == order_id).first()
    if query:
        a = query.cells
        return query
    return {"error": "Not Found"}

@router.get("/organization/{organization_id}")
async def get_order_group_organization(organization_id: int):
    query = session.query(OrderGroup).join(Organization).filter(Organization.id == organization_id).all()
    for i in query:
        a = i.__dict__
        zero = 0
        for j in session.query(Order).session.query(Order).join(OrderGroup).filter(OrderGroup.id == a["id"]):
            c = len(j.cells)
            zero += c
        a["cellsCount"] = zero
        a["orderCount"] = session.query(Order).join(OrderGroup).filter(OrderGroup.id == a["id"]).count()
    return query

@router.get("/groups/{group_id}")
async def get_order_group_id(group_id: int):
    #query = session.query(Order).join(OrderGroup).filter(OrderGroup.id == group_id).all()
    query = session.query(OrderGroup).options(selectinload(OrderGroup.orders)).filter(OrderGroup.id == group_id).first()
    if query:
        return query
    return {"error": "Not Found"}

@router.delete("/groups/{group_id}")
async def get_order_group_id_delete(group_id: int):
    query = session.query(OrderGroup).filter(OrderGroup.id == group_id).first()

    if query:
        session.delete(query)
        session.commit()
        return {"error": "OrderGroup ({}) deleted".format(query.id)}
    return {"error": "Not Found Order Group"}

@router.post("/")
async def create_order(order: OrderSchema):
    date = int(time.time())*1000
    query = Order(name=order.name, description=order.description, date=order.date, grid=order.grid,
                  cellCount=order.cellCount, way=order.way)

    if not query.date:
        query.date = int(time.time())*1000

    field = session.query(Field).filter(Field.id == order.fieldId).first()
    if not field:
        return {"error": "Not Found Field"}

    orderQuery = session.query(OrderGroup).filter(OrderGroup.id == order.orderGroupId).first()
    if orderQuery:
        #query.organization = orderQuery.organization

        #orderGroupsField = session.query(Field).join(Organization).join(OrderGroup).filter(OrderGroup.id == orderQuery.id).all()
        for j in session.query(Order).join(OrderGroup).filter(OrderGroup.id == orderQuery.id).all():
            print(j)
            for k in session.query(Field).join(Order).filter(Order.id == j.id).all():
                print(k)
                if field.id == k.id:
                    return {"error": "В данном заказе уже есть такое поле"}
        query.group = orderQuery
    else:
        organization = session.query(Organization).filter(Organization.id == order.organizationId).first()
        if not organization:
            return {"error": "Not Found Organization"}
        orderGroup = OrderGroup(name=organization.name+" | "+str(date)+" | "+str(organization.id), date=date, organization=organization)
        query.group = orderGroup
        query.organization = organization




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