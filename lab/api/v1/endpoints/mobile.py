from fastapi import APIRouter
from db import session
from lab.models.order import OrderGroup, Order
import io
from mapbox import Static
from starlette.responses import StreamingResponse


service = Static()
router = APIRouter()

@router.get('/geo_json_img/{id}')
async def get_img(id: int):
    query = session.query(Order).get(id)
    if query:
        json = query.grid
        response = service.image('mapbox.satellite', features=[json])
        return StreamingResponse(io.BytesIO(response.content), media_type="image/png")
    return {"error": "Not Found"}