from typing import List
from app.api.entities.category_entity import Category
from app.api.interfaces.marketplace_client_interface import ICategoryRepository
from app.api.infrastructure.orm.models.category_orm import MarketplaceEnum
from app.api.schemas.category import CategoryIn


class AddTreeCategoriesUseCase:
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    async def execute(self, ozon_data, wb_data):
        records = []
        visited_ozon_ids = set()

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

        def process_wb(nodes):
            for node in nodes:
                records.append({
                    "marketplace": MarketplaceEnum.WB,
                    "external_id": node.get("subjectID", node.get("id")),
                    "parent_external_id": node.get("parentID"),
                    "name": node.get("subjectName", node.get("name")),
                    "type_id": None
                })

        for root in ozon_data:
            process_ozon(root)

        process_wb(wb_data)

        # Получаем уже существующие категории
        existing_ids = await self.category_repo.get_existing_ids()
        filtered_records = [
            record for record in records
            if (record["marketplace"], record["external_id"]) not in existing_ids
        ]

        if filtered_records:
            await self.category_repo.add_categories_to_database(filtered_records)

