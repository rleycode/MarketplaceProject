from pydantic import BaseModel
from enum import Enum
from typing import Optional

class MarketplaceEnum(str, Enum):
    ozon = "ozon"
    wb = "wb"

class CategoryIn(BaseModel):
    marketplace: MarketplaceEnum
    external_id: int
    parent_external_id: Optional[int] = None
    name: str

class CategoryOut(CategoryIn):
    id: int