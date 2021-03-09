from fastapi import APIRouter

from lab.api.v1.endpoints import elements, samples, selection

api_router = APIRouter()

api_router.include_router(elements.router, tags=["Элементы"], prefix="/elements")
api_router.include_router(samples.router, tags=["Пробы"], prefix="/samples")
api_router.include_router(selection.router, tags=["Почвоотбор"], prefix="/selection")
