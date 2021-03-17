from db import session
from fastapi import APIRouter, Query
from lab.models.cells import Cells
from lab.models.elements import Elements
from lab.models.order import Order, OrderCells, OrderCellsResult
from lab.schemas.status import status_dict, StatusName
from lab.schemas.cells import OrderCellsResultSchema
import time

router = APIRouter()

@router.get("/results")
async def get_results():
    query = session.query(OrderCellsResult).all()
    return query

@router.get("/results/{order_id}")
async def get_cells_for_order(order_id: int):
    cells = session.query(OrderCellsResult).join(OrderCells).filter(OrderCells.orderId == order_id).all()
    for i in cells:
        a = i.orderCell
    return cells

@router.get("/{order_id}")
async def get_cells_for_order(order_id: int):
    cells = session.query(OrderCells).filter(OrderCells.orderId == order_id).all()
    for i in cells:
        a = i.cell.code
        print(a)
    return cells

@router.post("/result/{order_id}/{cell_code}")
async def create_result_for_cell(order_id: int, cell_code: int, orderCellsResultSchema: OrderCellsResultSchema):
    cell = session.query(OrderCells).join(Cells).filter(OrderCells.orderId == order_id, Cells.code == cell_code).first()
    element = session.query(Elements).filter(Elements.id == orderCellsResultSchema.elementId).first()
    if cell and element:
        date = int(time.time())*1000
        result = OrderCellsResult(orderCell=cell, element=element, result=orderCellsResultSchema.result, date=date)
        session.add(result)
        session.commit()
        return result

@router.get("/{cell_id}")
async def get_cells(order_id: int, cell_code: int):
    cell = session.query(OrderCells).join(Cells).filter(OrderCells.orderId == order_id, Cells.code == cell_code).first()
    if cell:
        a = cell.cell
        return cell

    query = session.query(Cells).filter(Cells.id == cell_code).first()
    if query:
        return query
    return {"error": "Not Found"}






@router.get("/status_name")
async def status_name():
    return status_dict

@router.get("/")
async def get_cells():
    query = session.query(OrderCells).all()
    for i in query:
        a = i.cell
        b = i.order
    return query

@router.post("/status/{order_id}/{cell_code}")
async def create_status_for_cell(order_id: int, cell_code: int, status: StatusName):
    cell = session.query(OrderCells).join(Cells).filter(OrderCells.orderId == order_id, Cells.code == cell_code).first()
    if cell:
        a = cell.cell
        cell.date = int(time.time())*1000
        cell.status = status
        return cell
    return {"error": "Not Found cell"}


