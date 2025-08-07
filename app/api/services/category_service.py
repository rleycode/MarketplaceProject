from typing import List
from app.api.entities.category_entity import Category
from app.api.infrastructure.marketplace_clients.yandex_client import YandexClient
from app.api.infrastructure.orm.models.models import MarketplaceEnum
from app.api.interfaces.marketplace_client_interface import ICategoryRepository
from app.api.schemas.category import CategoryIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.infrastructure.marketplace_clients.ozon_client import OzonClient
from app.api.infrastructure.marketplace_clients.wb_client import WbClient

class AddTreeCategoriesUseCase:
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    async def execute(self, ozon_data, wb_data, yandex_data):
        records = []
        visited_ozon_ids = set()

        # --- Обработка OZON ---
        def process_ozon(node, parent_id=None):
            node_id = node.get("description_category_id") or node.get("type_id")
            if node_id in visited_ozon_ids:
                return
            if node_id:
                visited_ozon_ids.add(node_id)

            if "description_category_id" in node:
                records.append({
                    "marketplace": MarketplaceEnum.OZON,
                    "external_id": node["description_category_id"],
                    "parent_external_id": parent_id,
                    "name": node["category_name"],
                    "type_id": node.get("type_id"),
                })
                parent_id = node["description_category_id"]
            elif "type_id" in node:
                records.append({
                    "marketplace": MarketplaceEnum.OZON,
                    "external_id": node["type_id"],
                    "parent_external_id": parent_id,
                    "name": node.get("type_name", "Без названия"),
                    "type_id": node["type_id"],
                })

            for child in node.get("children", []):
                process_ozon(child, parent_id)

        # --- Обработка WB ---
        def process_wb(nodes):
            for node in nodes:
                records.append({
                    "marketplace": MarketplaceEnum.WB,
                    "external_id": node.get("subjectID", node.get("id")),
                    "parent_external_id": node.get("parentID"),
                    "name": node.get("subjectName", node.get("name")),
                    "type_id": None
                })

        # --- Обработка YANDEX ---
        def process_yandex(node, parent_id=None):
            if node.get("id") is None:
                return
            records.append({
                "marketplace": MarketplaceEnum.YANDEX,
                "external_id": node["id"],
                "parent_external_id": parent_id,
                "name": node.get("name", "Без названия"),
                "type_id": None
            })
            for child in node.get("children") or []:
                if child:
                    process_yandex(child, node["id"])
        # Обрабатываем все источники
        for root in ozon_data:
            process_ozon(root)
        process_wb(wb_data)
        if yandex_data:
            process_yandex(yandex_data)

        # Фильтрация уже существующих
        existing_ids = await self.category_repo.get_existing_ids()
        filtered_records = [
            record for record in records
            if (record["marketplace"], record["external_id"]) not in existing_ids
        ]

        if filtered_records:
            await self.category_repo.add_categories_to_database(filtered_records)



class CategoryAttributesService:
    def __init__(self, category_repo: ICategoryRepository, wb_client: WbClient, ozon_client: OzonClient, yandex_client: YandexClient):
        self.category_repo = category_repo
        self.wb_client = wb_client
        self.ozon_client = ozon_client
        self.yandex_client = yandex_client  

    async def get_required_attributes(self, local_category_id: int) -> dict:
        category = await self.category_repo.get_category_by_id(local_category_id)
        if not category:
            return {"error": "Category not found"}

        attributes = {}

        # WB
        if category.wb_category and category.wb_category.external_id:
            wb_external_id = category.wb_category.external_id
            wb_attrs = await self.wb_client.get_category_attributes(wb_external_id)
            wb_required = [attr for attr in wb_attrs if attr.get("required") == True]
            attributes["wb"] = wb_required

        # OZON
        if (
            category.ozon_category and
            category.ozon_category.type_id and
            category.ozon_category.parent_external_id
        ):
            ozon_external_id = category.ozon_category.parent_external_id
            ozon_type_id = category.ozon_category.type_id

            ozon_attrs = await self.ozon_client.get_category_attributes(
                external_id=ozon_external_id,
                type_id=ozon_type_id
            )
            ozon_required = [attr for attr in ozon_attrs if attr.get("is_required")]
            attributes["ozon"] = ozon_required  # ✅ перемещено в правильное место

        # YANDEX
        if category.yandex_category and category.yandex_category.external_id:
            yandex_external_id = category.yandex_category.external_id
            yandex_attrs = await self.yandex_client.get_category_attributes(yandex_external_id)
            yandex_required = [attr for attr in yandex_attrs if attr.is_required]
            attributes["yandex"] = yandex_required

        return attributes
