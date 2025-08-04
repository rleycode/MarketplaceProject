from typing import List
from fastapi import UploadFile
import pandas as pd
from io import BytesIO
from app.api.infrastructure.marketplace_clients.ozon_client import OzonClient
from app.api.infrastructure.marketplace_clients.wb_client import WbClient
from app.api.infrastructure.orm.models.product_orm import Product
from app.api.interfaces.marketplace_client_interface import IProductRepository
from app.api.tasks.import_products import import_products_task

class ProductExportService:
    def __init__(self, product_repo: IProductRepository, wb_client: WbClient, ozon_client: OzonClient):
        self.product_repo = product_repo
        self.wb_client = wb_client
        self.ozon_client = ozon_client

    async def export_products_to_excel(self, category_id: int) -> bytes:
        # 1. Получаем товары из PIM
        products = await self.product_repo.get_products_by_category(category_id)

        # 2. Формируем список словарей
        product_dicts = [
            {
                "product_id": p.id,
                "title": p.title,
                "brand": p.brand,
                "used_sku": p.used_sku,
                "common_sku": p.common_sku,
                "ozon_sku": p.ozon_sku,
                "wb_sku": p.wb_sku,
            }
            for p in products
        ]

        # 3. Обновляем SKU с маркетплейсов
        updated = await self._fetch_existing_from_marketplaces(product_dicts)

        # 4. Генерируем Excel и возвращаем байты
        df = pd.DataFrame(updated)
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer.read()

    async def _fetch_existing_from_marketplaces(self, products: list[dict]) -> list[dict]:
        codes = [p["used_sku"] or p["common_sku"] for p in products]

        ozon_data = await self.ozon_client.get_existing_products(codes)  # {sku: ozon_sku}
        wb_data = await self.wb_client.get_existing_products(codes)      # {sku: wb_sku}

        for product in products:
            code = product["used_sku"] or product["common_sku"]
            product["ozon_sku"] = ozon_data.get(code)
            product["wb_sku"] = wb_data.get(code)

        return products
    
class ProductImportService:
    async def start_import_task(self, file: UploadFile) -> str:
        content = await file.read()
        task = import_products_task.delay(content)  # type: ignore
        return task.id