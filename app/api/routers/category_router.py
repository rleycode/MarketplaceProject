from fastapi import APIRouter, Depends
from typing import List
from app.api.services.category_service import CategoryService
from app.api.schemas.category import CategoryIn
from app.api.di.dependencies import get_category_service

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", summary="Получить список категорий")
async def get_all_categories(
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_all_categories()


@router.post("/", summary="Добавить категории")
async def add_categories(
    categories: List[CategoryIn],
    service: CategoryService = Depends(get_category_service)
):
    await service.save_categories(categories)
    return {"status": "ok", "count": len(categories)}
