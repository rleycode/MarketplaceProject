from typing import List, Optional
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
            },
            timeout=httpx.Timeout(20.0)
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
        data = {"description_category_id": external_id, "type_id": type_id, "language": "DEFAULT"}
        response = await self.client.post("/v1/description-category/attribute", json=data)
        print("❗ Ответ Ozon API:", response.status_code, response.text)
        response.raise_for_status()
        return response.json().get("result", [])
    
    async def get_existing_products(self, offer_ids: list[str]) -> dict:
        data = {"offer_id": offer_ids}
        response = await self.client.post("/v3/product/info/list", json=data)
        response.raise_for_status()
        result = response.json().get("items", [])
        return {item["offer_id"]: item["id"] for item in result if "offer_id" in item and "id" in item}

    async def get_product_list(
        self,
        offer_ids: Optional[List[str]] = None,
        product_ids: Optional[List[str]] = None,
        visibility: str = "ALL",
        last_id: str = "",
        limit: int = 100
    ):
        body = {
            "filter": {
                "visibility": visibility
            },
            "last_id": last_id,
            "limit": limit
        }

        if offer_ids:
            body["filter"]["offer_id"] = offer_ids
        elif product_ids:
            body["filter"]["product_id"] = product_ids

        response = await self.client.post("/v3/product/list", json=body)
        response.raise_for_status()
        return response.json()
        