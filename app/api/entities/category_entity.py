from typing import Optional

class Category:
    id: int
    name: str
    marketplace: str
    external_id: int
    parent_external_id: Optional[int]
