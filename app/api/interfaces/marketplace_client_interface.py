from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from app.api.infrastructure.orm.models.category_orm import MarketplaceCategory

class ICategoryRepository:
    async def get_existing_ids(self):
        raise NotImplementedError

    async def add_categories_to_database(self, categories):
        raise NotImplementedError

    async def get_category_by_id(self, local_category_id: int):
        raise NotImplementedError