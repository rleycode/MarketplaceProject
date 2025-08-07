from typing import List, Optional
from fastapi import UploadFile
import pandas as pd
from io import BytesIO
from app.api.infrastructure.marketplace_clients.ozon_client import OzonClient
from app.api.infrastructure.marketplace_clients.wb_client import WbClient
from app.api.interfaces.marketplace_client_interface import IProductRepository
from app.api.tasks.import_products import import_products_task

class ProductExportService:
    def __init__(self, product_repo: IProductRepository, wb_client: WbClient, ozon_client: OzonClient):
        self.product_repo = product_repo
        self.wb_client = wb_client
        self.ozon_client = ozon_client

    async def export_products_to_excel(self, category_id: int) -> bytes:
        products = await self.product_repo.get_products_by_category(category_id)
        brand_alias_map = await self._get_brand_alias_mapping()
        product_dicts = []
        for p in products:
            product_dicts.append({
                "id": p.id,
                "brand_id": p.brand_id,
                "used_sku": p.used_sku,
                "sku_1": p.sku_1,
                "sku_2": p.sku_2,
                "common_sku": p.common_sku,
                "part_number": p.part_number,
                "ozon_sku": p.ozon_sku,
                "ozon_id": p.ozon_id,
                "wb_id": p.wb_id,
                "yandex_id": p.yandex_id,
                "id_1c": p.id_1c,
                "id_mp": p.id_mp,
                "name": p.name,
                "description": p.description,
                "keywords": p.keywords,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "updated_at": p.updated_at.isoformat() if p.updated_at else None,
                "comment": p.comment,
                "size_id": p.size_id,
                "price_id": p.price_id,
                "media_id": p.media_id,
                "fitment_id": p.fitment_id,
                "type_id": p.type_id,
            })

        # 1. Получаем соответствия алиасов брендов (alias_name -> brand.name)
        brand_alias_map = await self._get_brand_alias_mapping()

        # Обновляем поле brand на основной бренд
        for product in product_dicts:
            alias = product.get("brand")
            if alias in brand_alias_map:
                product["brand"] = brand_alias_map[alias]

        # Обновляем SKU с маркетплейсов
        updated = await self._fetch_existing_from_marketplaces(product_dicts)

        df = pd.DataFrame(updated)
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer.read()

    async def _get_brand_alias_mapping(self) -> dict[str, str]:
        """
        Вернёт словарь {alias_name: main_brand_name} для всех алиасов брендов из БД.
        """
        result = await self.product_repo.get_brandsalias()
        rows = result.all() # type: ignore
        return {alias: brand for alias, brand in rows}

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