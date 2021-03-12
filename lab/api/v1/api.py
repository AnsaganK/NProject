from fastapi import APIRouter

from lab.api.v1.endpoints import elements, order
from app.api.v1.endpoints import organization, user, field
api_router = APIRouter()

api_router.include_router(elements.router, tags=["Элементы"], prefix="/elements")
api_router.include_router(organization.router, tags=["Организации"], prefix="/organizations")
api_router.include_router(user.router, tags=["Пользователи"], prefix="/users")
api_router.include_router(field.router, tags=["Поля"], prefix="/fields")
api_router.include_router(order.router, tags=["Заказы"], prefix="/orders")
