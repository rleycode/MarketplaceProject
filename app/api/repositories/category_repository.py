from sqlalchemy.orm import selectinload
from typing import List, Dict, Tuple
from sqlalchemy import Sequence, select
from sqlalchemy.dialects.postgresql import insert
from app.api.infrastructure.orm.models.models import MarketplaceCategory, Category
from app.api.interfaces.marketplace_client_interface import ICategoryRepository
from app.api.repositories.base import SQLAlchemyRepository

class CategoryRepository(SQLAlchemyRepository, ICategoryRepository):
    model = MarketplaceCategory

    async def get_existing_ids(self) -> set[Tuple[str, str]]:
        async with self.session as session:
            result = await session.execute(
                select(self.model.marketplace, self.model.external_id)
            )
            return {(str(row[0]), str(row[1])) for row in result.all()}

    async def add_categories_to_database(self, records: List[Dict]):
        async with self.session as session:
            async with session.begin():
                for i in range(0, len(records), 200):
                    batch = records[i:i + 200]
                    stmt = insert(self.model).values(batch).on_conflict_do_nothing(
                        index_elements=["marketplace", "external_id"]
                    )
                    await session.execute(stmt)
            await session.commit()

    async def get_all(self):
        async with self.session as session:
            result = await session.execute(select(self.model))
            return result.mappings().all()
        
    async def get_category_by_id(self, category_id: int) -> Category | None:
        result = await self.session.execute(
            select(Category)
            .where(Category.id == category_id)
            .options(
                selectinload(Category.ozon_category),
                selectinload(Category.wb_category),
                selectinload(Category.yandex_category)
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all_local_categories_with_mp_ids(self):
        result = await self.session.execute(
            select(Category).options(
                selectinload(Category.ozon_category),
                selectinload(Category.wb_category),
                selectinload(Category.yandex_category),
            )
        )
        categories = result.scalars().all()
        return categories