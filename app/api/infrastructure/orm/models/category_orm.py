from datetime import datetime
from sqlalchemy import BIGINT, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.api.infrastructure.orm.database import Base
from enum import Enum
from sqlalchemy import Enum as SQLEnum

class MarketplaceEnum(Enum):
    OZON = "OZON"
    WB = 'WB'
    YANDEX = 'YANDEX'
    
class MarketplaceCategory(Base):
    __tablename__ = "marketplace_categories"
    __table_args__ = (
    UniqueConstraint("marketplace", "external_id", name="uq_marketplace_external_id"),
)
    id: Mapped[int] = mapped_column(primary_key=True)
    marketplace: Mapped[MarketplaceEnum] = mapped_column(
    SQLEnum(MarketplaceEnum, name="marketplace_enum", create_type=True),
    nullable=False
)
    external_id: Mapped[int] = mapped_column(BIGINT)  # id категории на стороне МП
    parent_external_id: Mapped[int] = mapped_column(BIGINT, nullable=True)  # id родителя на стороне МП
    name: Mapped[str] = mapped_column(String)
    full_path: Mapped[str] = mapped_column(String, nullable=True)  # "Авто → Масла → Моторные"
    type_id: Mapped[int] = mapped_column(BIGINT, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    ozon_category_id = mapped_column(ForeignKey("marketplace_categories.id"), nullable=True)
    wb_category_id = mapped_column(ForeignKey("marketplace_categories.id"), nullable=True)

    ozon_category = relationship(
        "MarketplaceCategory",
        foreign_keys=[ozon_category_id],
        lazy="joined"
    )
    wb_category = relationship(
        "MarketplaceCategory",
        foreign_keys=[wb_category_id],
        lazy="joined"
    )
    