from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

class MarketplaceClientInterface(ABC):
    @abstractmethod
    async def get_tree_categories(self) -> list[dict]:
        ...

class ICategoryRepository(ABC):
    @abstractmethod
    async def get_existing_ids(self) -> set[Tuple[str, str]]:
        ...

    @abstractmethod
    async def add_categories_to_database(self, records: List[Dict]):
        ...
