from db import session
from fastapi import APIRouter, Depends, Query, Response, status
from lab.models.order import Order, OrderCells, OrderGroup, OrderCellsStatus
from app.models.organization import Organization
from lab.models.elements import Elements
from lab.models.cells import Cells
from lab.models.orderPoints import OrderPoints
from lab.models.status import Status
from lab.models.mini_status import MiniStatus
from app.models.field import Field
from app.models.role import Role
from lab.schemas.order import OrderSchema
from lab.schemas.order import OrderCellsStatusSchema
from lab.schemas.status import StatusName, StatusIdSchema
import time
from sqlalchemy.orm import selectinload, load_only
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from sqlalchemy import desc

router = APIRouter()


@router.get("/me/{role_id}")
async def get_my_order(role_id: int, token: str = Depends(JWTBearer())):
    decode = decodeJWT(token)
    print(decode)
    for i in decode["roles"]:
        role = session.query(Role).filter(Role.id == i["id"]).first()
        if role.id == role_id or role.name == "admin":
            status = session.query(Status).filter(Status.role_selection_id == role_id).first()
            miniStatus = session.query(MiniStatus).filter(MiniStatus.name == "Готово").first()
            orderCells = session.query(OrderCells).join(OrderCellsStatus).filter(
                OrderCellsStatus.statusId == status.id).filter(OrderCellsStatus.miniStatusId == miniStatus.id).all()
            print(status)
            print(orderCells)
            return orderCells
    return {"error": "У вас нет такой роли"}


def PointsToGeoJson(points):
    featureCollection = {"type": "FeatureCollection",
                         "features": []}
    pointsList = []
    for point in points:
        p = {"type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point["longitude"], point["latitude"]]
            },
            "properties": {"date": point["dateCreate"], "id": point["id"]}
            }
        pointsList.append(p)

    featureCollection["features"] = pointsList
    return featureCollection

@router.get("/selected_points/{order_id}")
async def get_points_for_order(order_id: int):
    query = session.query(OrderPoints).filter(OrderPoints.orderId == order_id).first()
    points = PointsToGeoJson(query.points)
    return points


@router.get("/groups/{group_id}")
async def get_order_group_id(group_id: int):
    # query = session.query(Order).join(OrderGroup).filter(OrderGroup.id == group_id).all()
    query = session.query(OrderGroup).options(selectinload(OrderGroup.elements)).options(
        selectinload(OrderGroup.orders)).filter(OrderGroup.id == group_id).first()
    for i in query.orders:
        i.__dict__['fieldName'] = i.field.name
    if query:
        return query
    return {"error": "Not Found"}


from sqlalchemy.orm import defer


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


@router.get("/{orderId}/{cellsCode}")
async def get_status_for_order_cells(orderId: int, cellsCode: int):
    currentStatus = session.query(OrderCellsStatus).join(OrderCells).join(Cells).filter(
        OrderCells.orderId == orderId).filter(Cells.code == cellsCode).order_by(OrderCellsStatus.id.desc()).first()
    statuses = session.query(OrderCellsStatus).options(selectinload(OrderCellsStatus.status)).options(
        selectinload(OrderCellsStatus.miniStatus)).join(OrderCells).join(Cells).filter(
        OrderCells.orderId == orderId).filter(Cells.code == cellsCode).all()
    return {"currentStatus": currentStatus, "history": statuses}


@router.get("/order_cells_status")
async def get_order_cells_status():
    OCSS = session.query(OrderCellsStatus).all()
    return OCSS


@router.post("/{orderId}/{cellsCode}")
async def create_status_for_Order_cells(orderId: int, cellsCode: int, ocss: OrderCellsStatusSchema):
    cell = session.query(OrderCells).join(Cells).filter(OrderCells.orderId == orderId).filter(
        Cells.code == cellsCode).first()
    status = session.query(Status).filter(Status.id == ocss.statusId).first()
    miniStatus = session.query(MiniStatus).filter(MiniStatus.id == ocss.miniStatusId).first()

    if not cell:
        return {"error": "Not Found Cell"}
    if not status:
        return {"error": "Not Found Status"}

    if not miniStatus:
        return {"error": "Not Found MiniStatus"}

    OCSS = OrderCellsStatus(orderCells=cell, status=status, miniStatus=miniStatus, date=int(time.time() * 1000))

    session.add(OCSS)
    session.commit()

    currentStatus = session.query(OrderCellsStatus).join(OrderCells).join(Cells).filter(
        OrderCells.orderId == orderId).filter(Cells.code == cellsCode).order_by(OrderCellsStatus.id.desc()).first()
    statuses = session.query(OrderCellsStatus).options(selectinload(OrderCellsStatus.status)).options(
        selectinload(OrderCellsStatus.miniStatus)).join(OrderCells).join(Cells).filter(
        OrderCells.orderId == orderId).filter(Cells.code == cellsCode).all()

    return {"currentStatus": currentStatus, "history": statuses}


@router.post("/status/")
async def get_cells_for_order(status: StatusIdSchema):
    print(status)
    print(OrderCells)
    # orderCells = session.query(OrderCells).filter(OrderCells.status == status).all()
    # orderCells = session.query(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.status == status).all()
    # cells = session.query(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.status == status).all()
    orderCells = session.query(OrderCells).join(Order).filter(OrderCells.status == status.status).subquery()
    orders = session.query(Order).join(orderCells).filter(OrderCells.orderId == Order.id).all()
    print(orders)
    return orders


@router.get("/groups")
async def get_order_group():
    query = session.query(OrderGroup).options(selectinload(OrderGroup.elements)).options(
        selectinload(OrderGroup.organization)).all()
    for i in query:
        a = i.__dict__
        zero = 0
        data = i.orders
        for j in data:
            c = len(j.cells)
            zero += c

        a["cellsCount"] = zero
        a["orderCount"] = len(data)
    return query


@router.get("/{order_id}")
async def get_order(order_id: int):
    query = session.query(Order).options(selectinload(Order.cells)).options(selectinload(Order.elements)).options(
        selectinload(Order.elements)).filter(Order.id == order_id).first()
    if query:
        for i in query.elements:
            print(i.types)
            for j in i.types:
                print(j)
        if len(query.points[0].points) != 0:
            query.__dict__["isPoints"] = True
        else:
            query.__dict__["isPoints"] = False
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


@router.put("/{order_id}")
async def update_order(order_id: int, order: OrderSchema):
    query = session.query(Order).filter(Order.id == order_id).first()

    query.name = order.name
    query.description = order.description
    query.date = order.date
    query.grid = order.grid
    query.cellCount = order.cellCount
    query.way = order.way

    orderGroup = session.query(OrderGroup).filter(OrderGroup.id == order.orderGroupId).first()
    query.group = orderGroup

    query.elements = []
    if order.date:
        query.date = order.date
    else:
        query.date = int(time.time()) * 1000

    field = session.query(Field).filter(Field.id == order.fieldId).first()
    if not field:
        return {"error": "Not Found Field"}
    query.field = field

    query.elements = []
    for i in order.elements:
        element = session.query(Elements).filter(Elements.id == i).first()
        if element:
            query.elements.append(element)

    session.add(query)
    session.commit()

    return {"id": query.id, "name": query.name, "date": query.date, "cellCount": query.cellCount,
            "organization": query.organization,
            "grid": query.grid, "elements": query.elements, "way": query.way}


@router.post("")
async def create_order(order: OrderSchema):
    date = int(time.time()) * 1000
    query = Order(name=order.name, description=order.description, date=order.date, grid=order.grid,
                  cellCount=order.cellCount, way=order.way)

    if not query.date:
        query.date = int(time.time()) * 1000

    field = session.query(Field).filter(Field.id == order.fieldId).first()
    if not field:
        return {"error": "Not Found Field"}

    orderQuery = session.query(OrderGroup).filter(OrderGroup.id == order.orderGroupId).first()
    if orderQuery:
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
        orderGroup = OrderGroup(name=organization.name + " | " + str(date) + " | " + str(organization.id), date=date,
                                organization=organization)

        for i in order.elements:
            element = session.query(Elements).filter(Elements.id == i).first()
            if element:
                orderGroup.elements.append(element)

        query.group = orderGroup
        query.organization = organization

    query.field = field
    for i in order.elements:
        element = session.query(Elements).filter(Elements.id == i).first()
        if element:
            query.elements.append(element)

    status = session.query(Status).filter(Status.name == "planned").first()
    for i in range(1, order.cellCount + 1):
        cell = Cells(code=i)
        date = int(time.time()) * 1000
        orderCells = OrderCells(order=query, cell=cell, date=date)
        session.add(orderCells)
        if status:
            OCS = OrderCellsStatus(orderCells=orderCells, status=status, date=int(time.time()) * 1000)
            session.add(OCS)
    session.add(query)
    session.commit()

    last_id = query.id
    organization = order.dict()

    return {**organization, "id": last_id}


@router.delete("/{order_id}")
async def delete_order(order_id: int):
    query = session.query(Order).filter(Order.id == order_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Order ({}) deleted".format(query.name)}
    return {"error": "Not Found"}
