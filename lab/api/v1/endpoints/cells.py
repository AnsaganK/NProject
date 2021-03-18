from db import session
from fastapi import APIRouter, Query
from lab.models.cells import Cells, CellsHistory
from lab.models.elements import Elements
from lab.models.order import Order, OrderCells, OrderCellsResult
from lab.schemas.status import status_dict, StatusName, StatusIdSchema
from lab.schemas.cells import OrderCellsResultSchema
import time
from sqlalchemy.orm import selectinload

router = APIRouter()

@router.get("/status_name")
async def status_name():
    return status_dict

@router.get("/history/{order_id}")
async def get_history(order_id: int):
    print(order_id)
    h = session.query(CellsHistory).join(OrderCells).filter(OrderCells.orderId == order_id).all()
    return h
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

#@router.get("/{order_id}")
#async def get_cells_for_order(order_id: int):
#    cells = session.query(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.orderId == order_id).all()
#    return cells


@router.get("/{order_id}")
async def get_cells_for_order(order_id: int):
    print(OrderCells.status)
    #orderCells = session.query(OrderCells).filter(OrderCells.status == status).all()
    #orderCells = session.query(OrderCells).join(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.status == status).all()
    cells = session.query(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.orderId == order_id).all()
    return cells

@router.post("/result/{order_id}/{cell_code}")
async def create_result_for_cell(order_id: int, cell_code: int, orderCellsResultSchema: OrderCellsResultSchema):
    cell = session.query(OrderCells).join(Cells).filter(OrderCells.orderId == order_id, Cells.code == cell_code).first()
    element = session.query(Elements).filter(Elements.id == orderCellsResultSchema.elementId).first()
    for i in session.query(OrderCellsResult).all():
        if i.orderCell == cell and i.element == element:
            return {"error": "A result with this name has already been created"}
    if cell and element:
        date = int(time.time())*1000
        result = OrderCellsResult(orderCell=cell, element=element, result=orderCellsResultSchema.result, date=date)
        session.add(result)
        session.commit()

        lastId = result.id
        orderCellsResultSchema = orderCellsResultSchema.dict()

        return {**orderCellsResultSchema, "id": lastId}

@router.get("/{order_id}/{cell_code}")
async def get_cells(order_id: int, cell_code: int):
    cell = session.query(OrderCells).join(Cells).filter(OrderCells.orderId == order_id, Cells.code == cell_code).first()
    if cell:
        a = cell.cell
        return cell

    query = session.query(Cells).filter(Cells.id == cell_code).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/status/{order_id}/{cell_code}")
async def create_status_for_cell(order_id: int, cell_code: int, status: StatusIdSchema):
    order_cell = session.query(OrderCells).options(selectinload(OrderCells.cell)).join(Cells).filter(OrderCells.orderId == order_id, Cells.code == cell_code).first()
    if order_cell:
        order_cell.date = int(time.time())*1000
        order_cell.status = status.status
        h = CellsHistory(order=order_cell, status=status.status)
        h.date = int(time.time())*1000
        session.add(h)
        session.commit()

        last_id = order_cell.id

        return {"id": last_id, "status": status.status}

    return {"error": "Not Found cell"}


@router.get("/")
async def get_cells():
    query = session.query(OrderCells).options(selectinload(OrderCells.cell)).all()
    return query




