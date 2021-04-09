from fastapi import APIRouter

from app.models.cars import Car
from app.models.organization import Organization
from app.schemas.cars import CarSchema, CarCreateSchema
from db import session
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("")
async def get_cars():
    query = session.query(Car).options(selectinload(Car.organization)).all()
    return query


@router.get("/{car_id}")
async def get_car(car_id: int):
    query = session.query(Car).options(selectinload(Car.organization)).filter(Car.id == car_id).first()
    return query


@router.post("", response_model=CarCreateSchema)
async def create_car(car: CarSchema):
    query = Car(**car.dict())
    organization = session.query(Organization).filter(Organization.id == car.organizationId).first()
    if organization:
        query.organization = organization
        session.add(query)
        session.commit()
        # query = query.__dict__['organization'] = organization
        return query
    return {"Организация не найдена"}


@router.delete("/{car_id}", response_model=CarCreateSchema)
async def delete_car(car_id: int):
    query = session.query(Car).options(selectinload(Car.organization)).get(car_id)
    if not query:
        return {"error": "Объект не найден"}
    session.add(query)
    session.commit()
    return query
