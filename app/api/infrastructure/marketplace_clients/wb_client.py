from app.api.core.config import setting
import httpx

class WbClient:
    BASE_URL = "https://content-api.wildberries.ru"
    
    def __init__(self, api_key: str = setting.WB_API_KEY):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": self.api_key
            }
        )
        
    async def get_parent_categories(self, locale: str = "ru") -> list[dict]:
        params = {"locale": locale}
        response = await self.client.get("/content/v2/object/parent/all", params=params)
        response.raise_for_status()
        return response.json()["data"] 