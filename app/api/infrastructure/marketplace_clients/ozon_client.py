from app.api.core.config import setting
import httpx

class OzonClient:
    BASE_URL = "https://api-seller.ozon.ru"

    def __init__(self, api_key=setting.OZON_API_KEY, client_id=setting.OZON_CLIENT_ID):
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Client-Id": client_id,
                "Api-Key": api_key,
                "Content-Type": "application/json"
            }
        )
    
    async def get_tree_categories(self) -> list[dict]:
        all_results = []
        last_id = None
        has_next = True

        while has_next:
            data = {
                "filter": {"visibility": "ALL"},
                "limit": 1000,
                "last_id": last_id
            }

            try:
                response = await self.client.post("/v1/description-category/tree", json=data)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                print(f"Ошибка {e.response.status_code}: {e.response.text}")
                raise

            json_data = response.json()
            result = json_data.get("result", [])
            all_results.extend(result)

            has_next = json_data.get("has_next", False)
            if has_next and result:
                last_id = result[-1]["id"]
        
        return all_results
    
    async def get_category_attributes(self, external_id: int, type_id: int) -> list[dict]:
        # Пример запроса, уточните путь и параметры под ваш API Ozon
        data = {"category_id": external_id, "type_id": type_id}
        response = await self.client.post("/v1/attribute/category", json=data)
        response.raise_for_status()
        return response.json().get("result", [])