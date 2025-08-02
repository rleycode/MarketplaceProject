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
        
    async def get_all_categories(self, locale: str = "ru") -> list[dict]:
        # Получаем корневые категории
        params = {"locale": locale}
        response = await self.client.get("/content/v2/object/parent/all", params=params)
        response.raise_for_status()
        parents = response.json()["data"]

        all_categories = []

        async def fetch_children(parent_id):
            params = {"locale": locale, "parentID": parent_id}
            resp = await self.client.get("/content/v2/object/all", params=params)
            resp.raise_for_status()
            children = resp.json()["data"]
            for child in children:
                all_categories.append(child)
                # Если у категории есть дети, рекурсивно получаем их
                if child.get("isParent"):
                    await fetch_children(child["id"])

        # Для каждой родительской категории рекурсивно получаем все подкатегории
        for parent in parents:
            all_categories.append(parent)
            await fetch_children(parent["id"])

        return all_categories