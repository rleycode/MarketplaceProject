from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.api.core.config import setting

async_engine = create_async_engine(setting.get_url_db)
sessionmaker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
