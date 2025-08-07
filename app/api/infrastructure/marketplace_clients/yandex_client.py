import httpx
from app.api.core.config import setting
from app.api.infrastructure.marketplace_clients.smock import MarketplaceAttribute

class YandexClient:
    BASE_URL = "https://api.partner.market.yandex.ru"

    def __init__(self, api_key: str = setting.YANDEX_API_KEY):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Api-Key": self.api_key,
                "Content-Type": "application/json",
                "User-Agent": "MarketplaceClient/1.0"
            },
        )

    async def get_tree_categories(self):
        try:    
            response = await self.client.post("/categories/tree", json={"language": "RU"})
            response.raise_for_status()
            return response.json()["result"]    
        except httpx.HTTPStatusError as e:  
            print(f"❌ Status: {e.response.status_code}")
            print(f"📦 Body: {e.response.text}")
            raise
    async def get_category_parameters(self, category_id: int):
        response = await self.client.get(f"/categories/{category_id}/parameters")
        response.raise_for_status()
        data = response.json()
        return data.get("result", [])

    async def get_category_attributes(self, category_id: str) -> list[MarketplaceAttribute]:
        return [
            MarketplaceAttribute(name="Бренд", is_required=True, type="string"),
            MarketplaceAttribute(name="Название модели", is_required=True, type="string"),
            MarketplaceAttribute(name="Цвет", is_required=False, type="string"),
        ]