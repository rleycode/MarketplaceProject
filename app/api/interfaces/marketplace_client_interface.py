from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from app.api.infrastructure.orm.models.category_orm import MarketplaceCategory

class ICategoryRepository(ABC):
    @abstractmethod
    async def get_existing_ids(self) -> set[Tuple[str, str]]: ...

    @abstractmethod
    async def add_categories_to_database(self, records: List[Dict]) -> None: ...

    @abstractmethod
    async def get_all(self) -> List[MarketplaceCategory]: ...
