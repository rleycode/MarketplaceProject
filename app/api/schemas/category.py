from pydantic import BaseModel
from enum import Enum
from typing import Optional

class SMarketplaceEnum(str, Enum):
    ozon = "ozon"
    wb = "wb"

class CategoryIn(BaseModel):
    marketplace: SMarketplaceEnum
    external_id: int
    parent_external_id: Optional[int] = None
    name: str

class CategoryOut(CategoryIn):
    id: int