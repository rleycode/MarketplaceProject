from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple

from app.api.infrastructure.orm.models.models import Category, MarketplaceCategory, Product


class ICategoryRepository(ABC):
    @abstractmethod
    async def get_existing_ids(self) -> set[Tuple[str, str]]: ...

    @abstractmethod
    async def add_categories_to_database(self, records: List[Dict]) -> None: ...

    @abstractmethod
    async def get_all(self) -> List[MarketplaceCategory]: ...

    @abstractmethod
    async def get_category_by_id(self, category_id: int) -> Optional[Category]:
        ...
        
class IProductRepository(ABC):
    @abstractmethod
    async def get_products(self, category_id: Optional[int] = None) -> List[Product]: ...
    
    @abstractmethod
    async def get_products_by_category(self, category_id: int) -> list[Product]: ...
    
    @abstractmethod
    async def get_brandsalias(self): ...
    
class IBrandRepository(ABC):
    @abstractmethod
    async def get_alias_mapping(self) -> Dict[str, str]: ...
    
    @abstractmethod
    async def get_brand_alias_mapping(self): ...