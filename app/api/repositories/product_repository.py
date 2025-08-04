from typing import List
from sqlalchemy import select
from app.api.infrastructure.orm.models.product_orm import Product
from app.api.interfaces.marketplace_client_interface import  IProductRepository
from app.api.repositories.base import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository, IProductRepository):
    model = Product
    
    async def get_products_by_category(self, category_id: int):
        result = await self.session.execute(
            select(Product).where(Product.type == category_id)
        )
        return result.scalars().all()

    async def get_products(self, category_id: int | None = None) -> List[Product]:
        raise NotImplementedError
