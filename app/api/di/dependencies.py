from app.api.repositories.category_repository import CategoryRepository
from app.api.services.category_service import CategoryService
from app.api.infrastructure.orm.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_category_repository(
    session: AsyncSession = Depends(get_async_session()),
) -> CategoryRepository:
    return CategoryRepository(session=session)

def get_category_service(
    repo: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    return CategoryService(repo)