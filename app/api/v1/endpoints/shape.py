from fastapi import APIRouter
from app.models.shape import Shape
from app.schemas.shape import ShapeSchema, ShapeCreateSchema
from db import session

router = APIRouter()


@router.get("")
async def get_all_shape_files():
    query = session.query(Shape).all()
    return query