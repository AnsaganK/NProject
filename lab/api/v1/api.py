from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer

from lab.api.v1.endpoints import elements, order, status, mini_status, cells, color, elementTypes, mobile
from app.api.v1.endpoints import organization, user, field, typesForField, role, login, season, culture, fieldCultureSeason, irrigationType, tillage, workType, workSubType, work
api_router = APIRouter()

api_router.include_router(login.router, tags=["Авторизация и Регистрация"], prefix="/auth")
api_router.include_router(work.router, tags=["Работы"], prefix="/works")
api_router.include_router(workType.router, tags=["Типы работ"], prefix="/work_types")
api_router.include_router(workSubType.router, tags=["Подтипы работ"], prefix="/work_subtypes")
api_router.include_router(season.router, tags=["Сезоны"], prefix="/seasons")
api_router.include_router(culture.router, tags=["Культуры"], prefix="/cultures")
api_router.include_router(irrigationType.router, tags=["Тип орошения"], prefix="/irrigation_types")
api_router.include_router(tillage.router, tags=["Обработка почвы"], prefix="/tillages")
api_router.include_router(fieldCultureSeason.router, tags=["Севооборот"], prefix="/crop_rotation")
api_router.include_router(elementTypes.router, tags=["Типы элементов"], prefix="/elementTypes") #dependencies=[Depends(JWTBearer())])
api_router.include_router(elements.router, tags=["Элементы"], prefix="/elements") #dependencies=[Depends(JWTBearer())])
api_router.include_router(organization.router, tags=["Организации"], prefix="/organizations") #dependencies=[Depends(JWTBearer())])
api_router.include_router(user.router, tags=["Пользователи"], prefix="/users")
api_router.include_router(field.router, tags=["Поля"], prefix="/fields") #dependencies=[Depends(JWTBearer())])
api_router.include_router(typesForField.router, tags=["Типы полей"], prefix="/field_types") #dependencies=[Depends(JWTBearer())])
api_router.include_router(order.router, tags=["Заказы"], prefix="/orders") #dependencies=[Depends(JWTBearer())])
api_router.include_router(cells.router, tags=["Ячейки"], prefix="/cells") #dependencies=[Depends(JWTBearer())])
api_router.include_router(color.router, tags=["Цвета"], prefix="/colors") #dependencies=[Depends(JWTBearer())])
api_router.include_router(status.router, tags=["Статусы"], prefix="/statuses") #dependencies=[Depends(JWTBearer())])
api_router.include_router(mini_status.router, tags=["МиниСтатусы"], prefix="/mini_statuses") #dependencies=[Depends(JWTBearer())])
api_router.include_router(role.router, tags=["Роли"], prefix="/roles")
api_router.include_router(mobile.router, tags=["Для мобильного приложения"], prefix="/mobile")