from typing import List
from sqlalchemy import select
from app.api.infrastructure.orm.models.models import Product, BrandAlias, Brand
from app.api.interfaces.marketplace_client_interface import  IProductRepository
from app.api.repositories.base import SQLAlchemyRepository
from sqlalchemy.orm import selectinload 

class ProductRepository(SQLAlchemyRepository, IProductRepository):
    model = Product
    
    async def get_products_by_category(self, category_id: int):
        stmt = (
            select(Product)
            .where(Product.type_id == category_id)
            .options(selectinload(Product.brand))
    )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_products(self, category_id: int | None = None):
        raise NotImplementedError


    async def get_brandsalias(self):    
        result = await self.session.execute(
            select(BrandAlias.alias_name, Brand.name)
            .join(Brand, BrandAlias.brand_id == Brand.id)
        )
        return result