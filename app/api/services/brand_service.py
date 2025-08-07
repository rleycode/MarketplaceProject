from typing import Any
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from app.api.interfaces.marketplace_client_interface import IBrandRepository

class BrandMatchingService:
    def __init__(self, brand_repo: IBrandRepository):
        self.brand_repo = brand_repo

    async def canonicalize_brands_in_excel(self, excel_bytes: bytes) -> pd.DataFrame:
        df = pd.read_excel(excel_bytes)

        if 'brand' not in df.columns:
            raise ValueError("В Excel отсутствует колонка 'brand'")

        alias_map = await self.brand_repo.get_brand_alias_mapping()

        def get_canon(name: str) -> str:
            canon = alias_map.get(name.strip().lower()) # type: ignore
            if canon is None:
                raise ValueError(f"Бренд '{name}' не найден в brand_aliases")
            return canon

        df['brand'] = df['brand'].apply(get_canon)
        return df
