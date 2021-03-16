from db import session
from fastapi import APIRouter, Query
from lab.models.cells import Cells
from lab.models.order import Order, OrderCells
from lab.models.status import Status
from lab.schemas.status import StatusIdSchema
import time

router = APIRouter()


@router.get("/")
async def get_cells():
    query = session.query(Cells).all()
    for i in query:
        print(i.order)
    return query


@router.get("/{cell_id}")
async def get_cells(cell_id: int):
    query = session.query(Cells).filter(Cells.id == cell_id).first()
    if query:
        return query
    return {"error": "Not Found"}

@router.post("/status/{order_id}/{cell_code}")
async def create_result_for_cell():

    return None

@router.post("/status/{order_id}/{cell_code}")
async def create_status_for_cell(order_id: int, cell_code: int, statusId: StatusIdSchema):
    s = session.query(Status).filter(Status.id == statusId.statusId).first()
    if not s:
        return {"error": "Not Found Status"}
    cell = session.query(Cells).filter(Cells.orderId == order_id).filter(Cells.code == cell_code).first()
    if cell:
        cell.status = s
        return cell
    return {"error": "Not Found Cell"}