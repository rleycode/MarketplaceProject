from app.api.core.config import setting
import httpx
import asyncio
from typing import Any, Dict, List, Optional

class WbClient:
    BASE_URL = "https://content-api.wildberries.ru"

    def __init__(self, api_key: str = setting.WB_API_KEY):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": self.api_key,
                "User-Agent": "Mozilla/5.0 (compatible; my-wb-client/1.0)"
            },
            timeout=httpx.Timeout(30.0)
        )
        self.lock = asyncio.Lock()  # 👈 обязательно создаём один lock на весь клиент

    async def get_all_categories(self, locale: str = "ru") -> List[dict]:
        params = {"locale": locale}
        response = await self.client.get("/content/v2/object/parent/all", params=params)
        response.raise_for_status()
        parents = response.json()["data"]

        all_categories = []

        async def fetch_children(parent_id: int, depth: int = 0):
            if depth > 10:
                return

            limit = 1000
            offset = 0
            while True:
                params = {"locale": locale, "parentID": parent_id, "limit": limit, "offset": offset}
                try:
                    resp = await self.client.get("/content/v2/object/all", params=params)
                    if resp.status_code == 429:
                        print(f"⚠️ 429 Too Many Requests for parentID={parent_id}. Waiting 5 seconds...")
                        await asyncio.sleep(5)
                        continue
                    resp.raise_for_status()
                except httpx.HTTPStatusError as e:
                    print(f"❌ Error fetching children for {parent_id}: {e}")
                    return

                await asyncio.sleep(0.3)  # Защита от бана

                children = resp.json()["data"]
                if not children:
                    break

                for child in children:
                    all_categories.append(child)
                    if child.get("isParent"):
                        await fetch_children(child["id"], depth + 1)

                if len(children) < limit:
                    break  # Конец данных, больше страниц нет
                offset += limit

        for parent in parents:
            all_categories.append(parent)
            await fetch_children(parent["id"])

        return all_categories

    async def get_category_attributes(self, subjectId: int) -> list[dict]:
        path = f"/content/v2/object/charcs/{subjectId}"
        response = await self.client.get(path, params={"locale": "ru"})
        return response.json().get("data", [])

    async def get_existing_products(self, vendor_codes: list[str]) -> dict:
        result_map = {}
        for chunk in [vendor_codes[i:i+100] for i in range(0, len(vendor_codes), 100)]:
            response = await self.client.post("/content/v2/get/cards/list", json={"vendorCodes": chunk})
            response.raise_for_status()
            data = response.json()
            
            items = data.get("cards")  # или "data", уточни в документации API
            
            if not items:
                items = []
            
            for item in items:
                result_map[item["vendorCode"]] = item["nmID"]
            
            await asyncio.sleep(0.2)
        return result_map

    async def get_cards_list(
        self,
        limit: int = 100,
        with_photo: int = -1,
        text_search: Optional[str] = None,
        tag_ids: Optional[List[int]] = None,
        allowed_categories_only: bool = True,
        object_ids: Optional[List[int]] = None,
        brands: Optional[List[str]] = None,
        imt_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Получить список карточек с поддержкой пагинации.
        """
        results = []
        cursor = {
            "limit": limit,
            "updatedAt": None,
            "nmID": None,
        }

        while True:
            settings = {
                "sort": {"ascending": False},
                "filter": {
                    "withPhoto": with_photo,
                    "allowedCategoriesOnly": allowed_categories_only,
                },
                "cursor": cursor
            }
            
            if text_search:
                settings["filter"]["textSearch"] = text_search
            if tag_ids:
                settings["filter"]["tagIDs"] = tag_ids
            if object_ids:
                settings["filter"]["objectIDs"] = object_ids
            if brands:
                settings["filter"]["brands"] = brands
            if imt_id:
                settings["filter"]["imtID"] = imt_id

            response = await self.client.post(
                "/content/v2/get/cards/list",
                json={"settings": settings}
            )
            response.raise_for_status()
            data = response.json()

            cards = data.get("cards", [])
            results.extend(cards)

            # Обновляем курсор для следующей страницы
            cursor_response = data.get("cursor", {})
            updated_at = cursor_response.get("updatedAt")
            nmID = cursor_response.get("nmID")

            if not updated_at or not nmID or len(cards) < limit:
                # Если меньше лимита в ответе — значит это последняя страница
                break

            cursor["updatedAt"] = updated_at
            cursor["nmID"] = nmID

        return results