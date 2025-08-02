from fastapi import APIRouter, Depends
from typing import List
from app.api.infrastructure.marketplace_clients.wb_client import WbClient
from app.api.services.category_service import AddTreeCategoriesUseCase, CategoryAttributesService
from app.api.schemas.category import CategoryIn
from app.api.di.dependencies import get_category_attributes_service, get_category_service, get_ozon_client, get_wb_client
from fastapi import APIRouter, Depends, HTTPException
from app.api.infrastructure.marketplace_clients.ozon_client import OzonClient
from fastapi import APIRouter, Depends, Response
from app.api.services.product_service import ProductExportService
from fastapi import UploadFile, File, BackgroundTasks
from app.api.services.product_service import ProductImportService

router = APIRouter(prefix="/categories", tags=["Categories"])

# @router.get("/", summary="Получить список категорий")
# async def get_all_categories(
#     service: CategoryService = Depends(get_category_service)
# ):
#     return await service.get_all_categories()


# @router.post("/", summary="Добавить категории")
# async def add_categories(
#     categories: List[CategoryIn],
#     service: CategoryService = Depends(get_category_service)
# ):
#     await service.save_categories(categories)
#     return {"status": "ok", "count": len(categories)}

@router.get("/get_marketplace_categories", summary="Получить категории с маркетплейсов")
async def get_marketplace_categories(
    ozon_client: OzonClient = Depends(get_ozon_client),
    wb_client: WbClient = Depends(get_wb_client),
    category_service: AddTreeCategoriesUseCase = Depends(get_category_service)
):
    ozon_categories = await ozon_client.get_tree_categories()
    wb_categories = await wb_client.get_all_categories()
    await category_service.execute(ozon_categories, wb_categories)
    
@router.get("/categories/{local_id}/required-attributes")
async def get_required_attributes(
    local_id: int,
    category_service: CategoryAttributesService = Depends(get_category_attributes_service),
):
    result = await category_service.get_required_attributes(local_id)
    return result
