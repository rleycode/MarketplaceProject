from fastapi import APIRouter, Depends
from typing import List
from app.api.services.category_service import CategoryService
from app.api.schemas.category import CategoryIn
from app.api.di.dependencies import get_category_service
from fastapi import APIRouter, Depends, HTTPException
from app.api.infrastructure.marketplace_clients.ozon_client import OzonClient


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

router = APIRouter(prefix="/ozon", tags=["ozon"])

@router.get("/categories")
async def get_ozon_categories(
    service: CategoryService = Depends(get_category_service)
):
    client = OzonClient()
    try:
        categories = await client.get_tree_categories()
        await service.save_categories(categories)
        return {"status": "ok", "count": len(categories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))