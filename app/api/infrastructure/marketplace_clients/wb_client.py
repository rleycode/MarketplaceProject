from app.api.core.config import setting
import httpx
import asyncio
from typing import List

class WbClient:
    BASE_URL = "https://content-api.wildberries.ru"

    def __init__(self, api_key: str = setting.WB_API_KEY):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={"Authorization": self.api_key}
        )

    async def get_all_categories(self, locale: str = "ru") -> List[dict]:
        params = {"locale": locale}
        response = await self.client.get("/content/v2/object/parent/all", params=params)
        response.raise_for_status()
        parents = response.json()["data"]

        all_categories = []

        async def fetch_children(parent_id: int, depth: int = 0):
            if depth > 10:
                return

            params = {"locale": locale, "parentID": parent_id}
            try:
                resp = await self.client.get("/content/v2/object/all", params=params)
                if resp.status_code == 429:
                    print(f"⚠️  429 Too Many Requests for parentID={parent_id}. Waiting 5 seconds...")
                    await asyncio.sleep(5)
                    return await fetch_children(parent_id, depth)
                resp.raise_for_status()
            except httpx.HTTPStatusError as e:
                print(f"❌ Error fetching children for {parent_id}: {e}")
                return

            await asyncio.sleep(0.3)  # Защита от бана
            children = resp.json()["data"]
            for child in children:
                all_categories.append(child)
                if child.get("isParent"):
                    await fetch_children(child["id"], depth + 1)

        for parent in parents:
            all_categories.append(parent)
            await fetch_children(parent["id"])

        return all_categories
    
    async def get_category_attributes(self, external_id: int) -> list[dict]:
    # Пример запроса, уточните путь и параметры под ваш API WB
        params = {"objectID": external_id}
        response = await self.client.get("/content/v2/object/required-attributes", params=params)
        response.raise_for_status()
        return response.json().get("data", [])