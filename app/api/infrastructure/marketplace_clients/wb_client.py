from app.api.core.config import setting
import httpx
import asyncio
from typing import List, Optional

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

    async def safe_get(self, url: str, params: dict):
        max_retries = 5
        retries = 0
        rate_limit_hits = 0

        while retries < max_retries:
            async with self.lock:
                try:
                    resp = await self.client.get(url, params=params)
                    print(f"↩️ {resp.status_code} {url} | Remaining: {resp.headers.get('X-Ratelimit-Remaining')}")
                    print(resp.text)

                    if resp.status_code == 429:
                        rate_limit_hits += 1
                        if rate_limit_hits >= 3:
                            raise Exception("🚫 Слишком много 429 подряд — остановка")

                        retry_after = int(resp.headers.get("X-Ratelimit-Retry", 5))
                        reset_after = int(resp.headers.get("X-Ratelimit-Reset", 10))
                        print(f"⏳ 429 Too Many Requests — sleeping {retry_after}s (reset in {reset_after}s)")
                        await asyncio.sleep(max(retry_after, reset_after))
                        continue

                    rate_limit_hits = 0

                    if resp.status_code == 409:
                        print("⚠️ 409 Conflict — засчитываем как 5 запросов")
                        await asyncio.sleep(1)

                    remaining = int(resp.headers.get("X-Ratelimit-Remaining", 1))
                    if remaining == 0:
                        retry_after = int(resp.headers.get("X-Ratelimit-Retry", 5))
                        print(f"❗ 0 remaining — ждем {retry_after}s")
                        await asyncio.sleep(retry_after)
                    elif remaining < 5:
                        await asyncio.sleep(1.5)
                    elif remaining < 15:
                        await asyncio.sleep(0.5)
                    else:
                        await asyncio.sleep(0.2)

                    resp.raise_for_status()
                    return resp

                except httpx.HTTPStatusError as e:
                    retries += 1
                    print(f"❌ Попытка {retries}, ошибка: {e}")
                    await asyncio.sleep(2)

        raise Exception("❌ Превышен лимит попыток safe_get")

    async def get_all_categories(self, locale: str = "ru") -> Optional[List[dict]]:
        parents_resp = await self.safe_get("/content/v2/object/parent/all", params={"locale": locale})
        parents = parents_resp.json()["data"]
        all_categories = {}
        visited = set()

        # Список нужных категорий (можно расширить или менять по точному имени)
        allowed_parents = {"Автозапчасти", "Автоаксессуары и дополнительное оборудование"}

        async def fetch_children(parent_id: int, parent_name: Optional[str] = None, depth=0):
            if depth > 15 or parent_id in visited:
                return
            visited.add(parent_id)

            url = "/content/v2/object/all"
            params = {"locale": locale, "parentID": parent_id}

            try:
                resp = await self.safe_get(url, params)
            except Exception as e:
                print(f"❌ Не удалось получить детей для {parent_id}: {e}")
                return

            children = resp.json().get("data", [])

            for child in children:
                cat_id = child["subjectID"]
                if cat_id in all_categories:
                    continue
                all_categories[cat_id] = {
                    "id": cat_id,
                    "name": child.get("subjectName", "Без названия"),
                    "parent_id": child["parentID"],
                    "parent_name": child.get("parentName", parent_name),
                    "is_parent": False
                }
                await fetch_children(cat_id, child.get("subjectName"), depth + 1)

        for parent in parents:
            parent_id = parent["id"]
            name = parent["name"]
            print(f"🔍 Проверяем {name} ({parent_id})")

            resp = await self.safe_get("/content/v2/object/all", params={"locale": "ru", "parentID": parent_id})
            children = resp.json().get("data", [])

            print(f"🧩 Найдено {len(children)} подкатегорий у '{name}' ({parent_id})")


            if name not in allowed_parents:
                # Пропускаем неподходящие категории
                continue

            all_categories[parent_id] = {
                "id": parent_id,
                "name": parent_name,
                "parent_id": None,
                "parent_name": None,
                "is_parent": True
            }
            await fetch_children(parent_id, parent_name)

        return list(all_categories.values())

    async def get_category_attributes(self, subjectId: int) -> list[dict]:
        path = f"/content/v2/object/charcs/{subjectId}"
        response = await self.safe_get(path, params={"locale": "ru"})
        return response.json().get("data", [])

    async def get_existing_products(self, vendor_codes: list[str]) -> dict:
        result_map = {}
        for chunk in [vendor_codes[i:i+100] for i in range(0, len(vendor_codes), 100)]:
            # Тут тоже можно реализовать safe_post при необходимости
            response = await self.client.post("/content/v2/get/cards/list", json={"vendorCodes": chunk})
            response.raise_for_status()
            for item in response.json():
                result_map[item["vendorCode"]] = item["nmID"]
            await asyncio.sleep(0.2)  # 🎯 по чуть-чуть регулируем темп, если много чанков
        return result_map
