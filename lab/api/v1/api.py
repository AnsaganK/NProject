from fastapi import APIRouter

from lab.api.v1.endpoints import elements, order, status, mini_status, cells, color
from app.api.v1.endpoints import organization, user, field, typesForField, role
api_router = APIRouter()

api_router.include_router(elements.router, tags=["Элементы"], prefix="/elements")
api_router.include_router(organization.router, tags=["Организации"], prefix="/organizations")
api_router.include_router(user.router, tags=["Пользователи"], prefix="/users")
api_router.include_router(field.router, tags=["Поля"], prefix="/fields")
api_router.include_router(typesForField.router, tags=["Типы полей"], prefix="/field_types")
api_router.include_router(order.router, tags=["Заказы"], prefix="/orders")
api_router.include_router(cells.router, tags=["Ячейки"], prefix="/cells")
api_router.include_router(color.router, tags=["Цвета"], prefix="/colors")
api_router.include_router(status.router, tags=["Статусы"], prefix="/statuses")
api_router.include_router(role.router, tags=["Роли"], prefix="/role")