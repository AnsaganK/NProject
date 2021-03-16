from fastapi import APIRouter

from app.api.v1.endpoints import permission, role, user, login, organization, field

api_router = APIRouter()


api_router.include_router(login.router, tags=["Авторизация и Регистрация"], prefix="/auth")
api_router.include_router(user.router, tags=["Пользователи"], prefix="/users")
api_router.include_router(role.router, tags=["Роли"], prefix="/roles")
api_router.include_router(permission.router, tags=["Права"], prefix="/permissions")
api_router.include_router(organization.router, tags=["Организации"], prefix="/organizations")
api_router.include_router(field.router, tags=["Поля"], prefix="/field")