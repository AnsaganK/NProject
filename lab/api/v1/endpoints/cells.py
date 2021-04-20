from pydantic.types import List

from db import session
from fastapi import APIRouter, Query, Body
from lab.models.cells import Cells, CellsHistory
from lab.models.elements import Elements, ElementType, ElementColor, RangeColor, Range, Color
from lab.models.order import Order, OrderCells, OrderCellsResult, OrderCellsStatus
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
    cells = session.query(OrderCellsResult).options(selectinload(OrderCellsResult.element)).join(OrderCells).filter(OrderCells.orderId == order_id).all()
    dic = []
    for cell in cells:
        cellCode = cell.orderCell.cell.code
        cellDic = {"cellCode": cell.orderCell.cell.code, "results":[]}
        for c in cells:
            if c.orderCell.cell.code == cellCode:
                el = c.element
                cellDic["results"].append({"element": {"id":el.id, "code": el.code, "name": el.name}, "value": c.result})
        if cellDic not in dic:
            dic.append(cellDic)
    return dic

def getForOrderResultColor(order_id):
    all_els = []
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        for el in order.elements:
            onlyElement = {"element": el.name, "elementId": el.id, "result": []}
            cells = session.query(OrderCellsResult).options(selectinload(OrderCellsResult.element)).join(OrderCells).filter(
                OrderCells.orderId == order_id).filter(OrderCellsResult.elementId == el.id).all()
            for cell in cells:
                cellCode = cell.orderCell.cell.code
                for c in cells:
                    if c.orderCell.cell.code == cellCode:
                        pass
            dic = []
            types = session.query(ElementType).join(Elements).filter(Elements.id == el.id).all()
            for i in types:
                elDic = {"name": i.type.name, "id": i.type.id, "cells": []}
                for cell in cells:
                    cellCode = cell.orderCell.cell.code
                    cellResult = cell.result
                    cellColor = changeColor(i.color, cellResult)
                    colorDic = {"cellCode": cellCode, "cellResult": cellResult, "cellColor": cellColor}
                    elDic["cells"].append(colorDic)
                dic.append(elDic)
                onlyElement["result"].append(dic)
            all_els.append(onlyElement)
    return {"orderId": order_id, "results": all_els}

@router.post("/resultColor")
async def result_color_selected_orders(orderList:List[int] = Body(...)):
    dataList = []
    for orderId in orderList:
        data = getForOrderResultColor(orderId)
        dataList.append(data)
    return dataList

@router.get("/resultColor/{order_id}")
async def resultColor(order_id: int):
    return getForOrderResultColor(order_id)


def changeColor(elementColor, value):
    for i in elementColor:
        if i.rangeColor.range.of<=value and i.rangeColor.range.to>value:
            return i.rangeColor.color.code
    return None

@router.get("/resultColor/{order_id}/{element_id}")
async def resultColor(order_id: int, element_id: int):
    cells = session.query(OrderCellsResult).options(selectinload(OrderCellsResult.element)).join(OrderCells).filter(
        OrderCells.orderId == order_id).filter(OrderCellsResult.elementId == element_id).all()
    for cell in cells:

        cellCode = cell.orderCell.cell.code
        for c in cells:
            if c.orderCell.cell.code == cellCode:
                pass
    dic = []
    types = session.query(ElementType).join(Elements).filter(Elements.id == element_id).all()
    for i in types:
        elDic = {"name": i.type.name, "id": i.type.id, "cells": []}
        for cell in cells:
            cellCode = cell.orderCell.cell.code
            cellResult = cell.result
            cellColor = changeColor(i.color, cellResult)
            colorDic = {"cellCode": cellCode, "cellResult": cellResult, "cellColor": cellColor}
            elDic["cells"].append(colorDic)
        dic.append(elDic)
    return dic

#@router.get("/{order_id}")
#async def get_cells_for_order(order_id: int):
#    cells = session.query(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.orderId == order_id).all()
#    return cells


@router.get("/{order_id}")
async def get_cells_for_order(order_id: int):
    #orderCells = session.query(OrderCells).filter(OrderCells.status == status).all()
    #orderCells = session.query(OrderCells).join(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.status == status).all()
    cells = session.query(OrderCells).options(selectinload(OrderCells.cell)).filter(OrderCells.orderId == order_id).all()
    for i in cells:
        st = session.query(OrderCellsStatus).join(OrderCells).filter(OrderCells.id == i.id).order_by(OrderCellsStatus.id.desc()).first()
        if st:
            if st.status:
                statusName = st.status.name
            else:
                statusName = None
            if st.miniStatus:
                miniStatusName = st.miniStatus.name
            else:
                miniStatusName = None
            i.__dict__["currentStatus"] = {"statusName":statusName, "miniStatusName": miniStatusName}
    return cells

@router.post("/result/{order_id}/{cell_code}")
async def create_result_for_cell(order_id: int, cell_code: int, orderCellsResultSchema: OrderCellsResultSchema):
    order = session.query(Order).filter(Order.id == order_id).first()
    cell = session.query(OrderCells).join(Cells).filter(OrderCells.orderId == order_id, Cells.code == cell_code).first()
    for r in orderCellsResultSchema.results:
        element = session.query(Elements).filter(Elements.id == r.elementId).first()
        if element not in order.elements:
            return {"error": "Данного элемента нет в поле этой ячейки"}
        isElement = session.query(OrderCellsResult).filter(OrderCellsResult.elementId == element.id).filter(OrderCellsResult.orderCellId == cell.id).first()
        #for i in session.query(OrderCellsResult).all():
        #    if i.orderCell == cell and i.element == element:
        #        return {"error": "Для данной ячейки уже существутет запись с этим элементом"}
        if cell and element:
            date = int(time.time())*1000
            if not isElement:
                result = OrderCellsResult(orderCell=cell, element=element, result=r.value, date=date)
                session.add(result)
    session.commit()
    orderCellsResultSchema = orderCellsResultSchema.dict()

    return {**orderCellsResultSchema}

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




