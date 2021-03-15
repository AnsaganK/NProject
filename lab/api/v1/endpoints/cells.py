from db import session
from fastapi import APIRouter, Query
from lab.models.cells import Cells
from lab.models.order import Order, OrderCells
import time

router = APIRouter()


@router.get("/")
async def get_cells():
    query = session.query(Cells).all()
    for i in query:
        a = i.status
        b = i.orders
    return query


@router.get("/{cell_id}")
async def get_cells(cell_id: int):
    query = session.query(Cells).filter(Cells.id == cell_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/{order_id}/{cell_code}")
async def create_status_for_cell(order_id: int, cell_code: int):
    order = session.query(Order).filter(Order.id == order_id).first()
    orderCell = order.cells
    print(orderCell)


    cell = session.query(Cells).filter(Cells.code == cell_code).first()
    order_cells = session.query(OrderCells).filter(OrderCells.OrderId == order).filter(OrderCells.CellId == cell).first()
