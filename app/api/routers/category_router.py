from io import BytesIO
from fastapi import APIRouter, Depends
from typing import List

import pandas as pd
from app.api.infrastructure.marketplace_clients.wb_client import WbClient
from app.api.infrastructure.marketplace_clients.yandex_client import YandexClient
from app.api.services.category_service import AddTreeCategoriesUseCase, CategoryAttributesService
from app.api.schemas.category import CategoryIn
from app.api.di.dependencies import get_category_attributes_service, get_category_service, get_ozon_client, get_wb_client, get_yandex_client
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
    yandex_client: YandexClient = Depends(get_yandex_client),
    category_service: AddTreeCategoriesUseCase = Depends(get_category_service)
):
    print("Категории озон")
    ozon_categories = await ozon_client.get_tree_categories()
    print("Категории вб")
    wb_categories = await wb_client.get_all_categories()
    print("Категории яндекс")
    yandex_categories = await yandex_client.get_tree_categories()
    print("В базу данных")
    await category_service.execute(ozon_categories, wb_categories, yandex_categories)

@router.get("/categories/{local_id}/required-attributes")
async def get_required_attributes(
    local_id: int,
    category_service: CategoryAttributesService = Depends(get_category_attributes_service),
):
    result = await category_service.get_required_attributes(local_id)
    return result

@router.post("/complete", summary="Добавить обязательные атрибуты в Excel-шаблон")
async def complete_template_with_attributes(
    file: UploadFile = File(...),
    attr_service: CategoryAttributesService = Depends(get_category_attributes_service),
):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))

    if "type_id" not in df.columns:
        return {"error": "В Excel-файле не найден столбец 'type_id'"}

    type_ids = df["type_id"].dropna().unique().tolist()

    all_attributes = set()

    for type_id in type_ids:
        attributes = await attr_service.get_required_attributes(local_category_id=int(type_id))

        for mp in ["ozon", "wb", "yandex"]:
            names = [attr.get("name") for attr in attributes.get(mp, []) if attr.get("name")]
            all_attributes.update(names)

    # Добавляем недостающие колонки
    for col in all_attributes:
        if col not in df.columns:
            df[col] = ""

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=completed_template.xlsx"},
    )