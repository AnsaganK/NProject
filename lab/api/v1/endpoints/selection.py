from . import session
from fastapi import APIRouter, Depends
from lab.models.selection import Selection
from lab.schemas.selection import SelectionSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from fastapi.security import HTTPBearer
import time

router = APIRouter()


@router.get("/")
async def get_selection():
    query = session.query(Selection).all()
    return query


@router.get("/{element_id}")
async def get_element(element_id: int):
    query = session.query(Selection).filter(Selection.id == element_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_element(element: SelectionSchema):
    query = Selection(name=element.name, code=element.code, date=element.date)
    if not query.date:
        query.date = time.time()
    for i in session.query(Selection).all():
        if i.name == element.name:
            return {"error": "A element with this name has already been created"}

    session.add(query)
    session.commit()

    last_id = query.id
    organization = element.dict()

    return {**organization, "id": last_id}

