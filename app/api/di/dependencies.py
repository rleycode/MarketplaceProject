from app.api.infrastructure.marketplace_clients.ozon_client import OzonClient
from app.api.infrastructure.marketplace_clients.wb_client import WbClient
from app.api.repositories.category_repository import CategoryRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from collections.abc import AsyncGenerator
from app.api.services.category_service import AddTreeCategoriesUseCase
from app.api.infrastructure.orm.database import sessionmaker

# Здесь должен быть асинхронный генератор!
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session

async def get_category_repository(
    session: AsyncSession = Depends(get_async_session),
) -> CategoryRepository:
    return CategoryRepository(session=session)

def get_ozon_client() -> OzonClient:
    return OzonClient()

def get_wb_client() -> WbClient:
    return WbClient()

def get_category_service(
    category_repo: CategoryRepository = Depends(get_category_repository)
) -> AddTreeCategoriesUseCase:
    return AddTreeCategoriesUseCase(category_repo=category_repo)