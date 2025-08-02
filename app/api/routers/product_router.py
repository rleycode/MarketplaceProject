from fastapi import APIRouter, Depends
from typing import List, Optional
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

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/export", summary="Выгрузить товары в Excel")
async def export_products(
    category_id: Optional[int] = None,
    service: ProductExportService = Depends()
):
    excel_bytes = await service.export_products_to_excel(category_id)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=products.xlsx"}
    )
    
@router.post("/import", summary="Импорт товаров из Excel")
async def import_products(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    service: ProductImportService = Depends()
):
    task_id = await service.start_import_task(file)
    return {"task_id": task_id}