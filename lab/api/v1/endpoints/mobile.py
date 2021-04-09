from fastapi import APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import selectinload

from app.models.organization import Organization
from db import session
from lab.models.order import OrderGroup, Order

router = APIRouter()


@router.get("/organizations")
async def get_organizations():
    organizations = session.query(Organization).all()
    return {"organizations": organizations}


@router.get("/order_groups")
async def get_order_group():
    query = session.query(OrderGroup).order_by(desc(OrderGroup.date)).options(
        selectinload(OrderGroup.organization)).options(selectinload(OrderGroup.orders)).all()
    for i in query:
        a = i.__dict__
        zero = 0
        for j in session.query(Order).join(OrderGroup).filter(
                OrderGroup.id == a["id"]):
            c = len(j.cells)
            zero += c

        a["cellsCount"] = zero
        a["orderCount"] = session.query(Order).join(OrderGroup).filter(OrderGroup.id == a["id"]).count()
    return {"orders": query}


def parse_data(geoJson):
    data = geoJson["features"][0]["geometry"]["coordinates"]
    lst = []
    for i in data:
        a = [float(round(i[0], 7)), float(round(i[1], 7))]
        lst.append(a)
    geoJson["features"][0]["geometry"]["coordinates"] = lst
    return geoJson


def create_feature_collection(orders):
    print(orders)
    dic = {"type": "FeatureCollection", "features": []}
    features = []
    for i in orders:
        featureList = i.grid["features"]
        for j in featureList:
            features.append(j)
    dic["features"] = features
    return dic

@router.get("/groupGeoJson/{order_group_id}")
async def get_geojson_for_field(order_group_id: int):
    order = session.query(OrderGroup).filter(OrderGroup.id == order_group_id).first()
    if order:
        return create_feature_collection(order.orders)
    else:
        return {"error": "Поле не найдено"}


@router.get("/geojson/{order_id}")
async def get_geojson_for_field(order_id: int):
    order = session.query(Order).get(order_id)
    if order:
        return order.grid
    else:
        return {"error": "Поле не найдено"}


@router.get("/orders/{organization_id}")
async def get_orders_for_organization(organization_id: int):
    query = session.query(OrderGroup).filter(OrderGroup.organizationId == organization_id).all()
    return {"orders": query}
