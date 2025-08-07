from typing import Optional
from fastapi import APIRouter, Depends, Response
from app.api.di.dependencies import get_ozon_client, get_product_service, get_wb_client
from app.api.infrastructure.marketplace_clients.ozon_client import OzonClient
from app.api.infrastructure.marketplace_clients.wb_client import WbClient
from app.api.services.product_service import ProductExportService
from fastapi import UploadFile, File, BackgroundTasks

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/export", summary="Выгрузить товары в Excel")
async def export_products(
    local_category_id: int,
    service: ProductExportService = Depends(get_product_service),
):
    excel_bytes = await service.export_products_to_excel(local_category_id)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=products.xlsx"}
    )

    
# @router.post("/import", summary="Импорт товаров из Excel")
# async def import_products(
#     background_tasks: BackgroundTasks,
#     file: UploadFile = File(...),
#     service: ProductImportService = Depends()
# ):
#     task_id = await service.start_import_task(file)
#     return {"task_id": task_id}

@router.get("get-product-list", summary="Получить список товаров")
async def get_product_list(
    OzonClient: OzonClient = Depends(get_ozon_client),
    WbClient: WbClient = Depends(get_wb_client)
):
    ozon = await OzonClient.get_product_list()
    wb =  await WbClient.get_cards_list()
    return {"ozon": ozon, "wb": wb}