from app.api.infrastructure.marketplace_clients.ozon_client import OzonClient
from app.api.infrastructure.marketplace_clients.wb_client import WbClient
from app.api.repositories.category_repository import CategoryRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from collections.abc import AsyncGenerator
from app.api.repositories.product_repository import ProductRepository
from app.api.services.category_service import AddTreeCategoriesUseCase, CategoryAttributesService
from app.api.infrastructure.orm.database import sessionmaker
from app.api.services.product_service import ProductExportService

# Здесь должен быть асинхронный генератор!
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session

async def get_category_repository(
    session: AsyncSession = Depends(get_async_session),
) -> CategoryRepository:
    return CategoryRepository(session=session)

async def get_product_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ProductRepository:
    return ProductRepository(session=session)

def get_ozon_client() -> OzonClient:
    return OzonClient()

def get_wb_client() -> WbClient:
    return WbClient()

def get_category_service(
    category_repo: CategoryRepository = Depends(get_category_repository)
) -> AddTreeCategoriesUseCase:
    return AddTreeCategoriesUseCase(category_repo=category_repo)

def get_category_attributes_service(
    category_repo: CategoryRepository = Depends(get_category_repository),
    ozon_client: OzonClient = Depends(get_ozon_client),
    wb_client: WbClient = Depends(get_wb_client)
) -> CategoryAttributesService:
    return CategoryAttributesService(
        category_repo=category_repo,
        ozon_client=ozon_client,
        wb_client=wb_client
    )
    
def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository),
    ozon_client: OzonClient = Depends(get_ozon_client),
    wb_client: WbClient = Depends(get_wb_client)
) -> ProductExportService:
    return ProductExportService(
        product_repo=product_repo,         
        ozon_client=ozon_client,
        wb_client=wb_client,
    )