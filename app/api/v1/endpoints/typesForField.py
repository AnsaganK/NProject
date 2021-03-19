from fastapi import APIRouter
from db import session
from app.models.typesForField import TypesForField
from app.schemas.typesForField import TypesForFieldSchema

router = APIRouter()

@router.get("/")
async def get_types_for_field():
    query = session.query(TypesForField).all()
    return query

@router.get("/{type_id}")
async def get_type_for_field(type_id: int):
    query = session.query(TypesForField).filter(TypesForField.id == type_id).first()
    if query:
        return query
    return {"error": "Not Found type"}

@router.post("/")
async def create_type_for_field(type: TypesForFieldSchema):
    query = TypesForField(name=type.name, key=type.key)
    for i in session.query(TypesForField).all():
        if i.name == type.name and i.key == type.key:
            return {"error": "A type with this name and key has already been created"}
    session.add(query)
    session.commit()

    last_id = query.id
    type = type.dict()

    return {**type, "id": last_id}

