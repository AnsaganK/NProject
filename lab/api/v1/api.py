from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer

from lab.api.v1.endpoints import elements, order, status, mini_status, cells, color
from app.api.v1.endpoints import organization, user, field, typesForField, role, login
api_router = APIRouter()

api_router.include_router(login.router, tags=["Авторизация и Регистрация"], prefix="/auth")
api_router.include_router(elements.router, tags=["Элементы"], prefix="/elements", dependencies=[Depends(JWTBearer())])
api_router.include_router(organization.router, tags=["Организации"], prefix="/organizations", dependencies=[Depends(JWTBearer())])
api_router.include_router(user.router, tags=["Пользователи"], prefix="/users")
api_router.include_router(field.router, tags=["Поля"], prefix="/fields", dependencies=[Depends(JWTBearer())])
api_router.include_router(typesForField.router, tags=["Типы полей"], prefix="/field_types", dependencies=[Depends(JWTBearer())])
api_router.include_router(order.router, tags=["Заказы"], prefix="/orders", dependencies=[Depends(JWTBearer())])
api_router.include_router(cells.router, tags=["Ячейки"], prefix="/cells", dependencies=[Depends(JWTBearer())])
api_router.include_router(color.router, tags=["Цвета"], prefix="/colors", dependencies=[Depends(JWTBearer())])
api_router.include_router(status.router, tags=["Статусы"], prefix="/statuses", dependencies=[Depends(JWTBearer())])
api_router.include_router(mini_status.router, tags=["МиниСтатусы"], prefix="/mini_statuses", dependencies=[Depends(JWTBearer())])
api_router.include_router(role.router, tags=["Роли"], prefix="/roles")