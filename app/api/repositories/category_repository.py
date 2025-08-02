from typing import List, Dict, Tuple
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.api.infrastructure.orm.models.category_orm import MarketplaceCategory, MarketplaceEnum
from app.api.interfaces.marketplace_client_interface import ICategoryRepository
from app.api.repositories.base import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository, ICategoryRepository):
    model = MarketplaceCategory

    async def get_existing_ids(self) -> set[Tuple[MarketplaceEnum, int]]:
        async with self.session as session:
            result = await session.execute(
                select(self.model.marketplace, self.model.external_id)
            )
            rows = result.all()
            return {(row[0], row[1]) for row in result.all()}

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
