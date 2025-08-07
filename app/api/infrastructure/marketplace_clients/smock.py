from pydantic import BaseModel

class MarketplaceAttribute(BaseModel):
    name: str
    is_required: bool
    type: str