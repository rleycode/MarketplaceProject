
from sqlalchemy import select
from app.api.infrastructure.orm.models.models import Brand, BrandAlias
from app.api.interfaces.marketplace_client_interface import IBrandRepository
from app.api.repositories.base import SQLAlchemyRepository


class BrandRepository(SQLAlchemyRepository, IBrandRepository):
    model = Brand
    
    async def get_alias_mapping(self) -> dict[str, str]:
        stmt = select(BrandAlias.alias_name, Brand.name).join(Brand, Brand.id == BrandAlias.brand_id)
        result = await self.session.execute(stmt)
        return {row[0].lower(): row[1] for row in result.all()}
    
    async def get_brand_alias_mapping(self) -> dict[str, str]:
        stmt = (
            select(BrandAlias.alias_name, Brand.name)
            .join(Brand, Brand.id == BrandAlias.brand_id)
        )
        result = await self.session.execute(stmt)
        return {alias.lower(): brand for alias, brand in result.all()}