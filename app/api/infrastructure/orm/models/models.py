from datetime import datetime
from sqlalchemy import BIGINT, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.api.infrastructure.orm.database import Base
from sqlalchemy import Enum as SQLEnum
from enum import Enum

class MarketplaceEnum(Enum):
    OZON = "OZON"
    WB = 'WB'
    YANDEX = 'YANDEX'
        
class Characteristics(Base):
    __tablename__ = "characteristics"
    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[int] = mapped_column(Integer) #Вес в упаковке, г*
    height: Mapped[int] = mapped_column(Integer) #Высота упаковки, мм*
    width: Mapped[int] = mapped_column(Integer) #Ширина упаковки, мм*
    length: Mapped[int] = mapped_column(Integer) #Длина упаковки, мм
    box_size: Mapped[int] = mapped_column(Integer) #Индивидуальная коробка, (S, M, L)
    country: Mapped[str] = mapped_column(String) #Страна-изготовитель:Lynx Япония, DAN РФ, Suffix Китай
    quantity_text: Mapped[str] = mapped_column(String) #Комплектация (OZON)
    quantity_number: Mapped[int] = mapped_column(Integer) #Количество заводских упаковок (OZON)
    tn_ved: Mapped[str] = mapped_column(String) #ТН ВЭД коды ЕАЭС (OZON)
    guarantee: Mapped[int] = mapped_column(Integer) #Гарантийный срок, 	все товары 1 год гарантии (OZON)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="size")

# class WipersChars(Base):
#     __tablename__ = "wipers_chars"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String)    

"""
Кроссы
"""
class Cross(Base):
    __tablename__ = 'oem'
    id: Mapped[int] = mapped_column(primary_key=True)
    oem_brand: Mapped[str] = mapped_column(String) #OEM-номер (старая инфа, пересмотреть), ОЕМ Бренд
    oem_sku: Mapped[str] = mapped_column(String) #OEM-номер (старая инфа, пересмотреть, ОЕМ артикул
    cross_brand: Mapped[str] = mapped_column(String) #OEM-номер (старая инфа, пересмотреть), Бренд аналога
    cross_sku: Mapped[str] = mapped_column(String) #OEM-номер (старая инфа, пересмотреть), Артикул аналога
    
"""
Применяемость для заголовков/описаний и WB полей Марка автомобиля и Модель
"""
class Fitment(Base):
    __tablename__ = 'fitment'

    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(String) #Марка eng, Марка
    make_translit: Mapped[str] = mapped_column(String) #Марка ru
    model: Mapped[str] = mapped_column(String) #Модель eng, Модель
    model_translit: Mapped[str] = mapped_column(String) #Модель ru
    body: Mapped[str] = mapped_column(String) #Номер кузова, Кузов
    year_1: Mapped[int] = mapped_column(Integer) #Год начала
    year_2: Mapped[int] = mapped_column(Integer) #Год окончания
    engine: Mapped[str] = mapped_column(String) #Модификация двигателя
    power: Mapped[int] = mapped_column(Integer) #Мощность
    engine_capacity: Mapped[int] = mapped_column(Integer) #Объем двигателя
    engine_code: Mapped[str] = mapped_column(String) #Код двигателя

    products: Mapped[list["Product"]] = relationship("Product", back_populates="fitment")

    
"""
Для чего подходит и фильтр в категории, выпадающий список - Техническая таблица
"""    
class OzonFitment(Base):
    __tablename__ = 'ozon_fitment'

    id: Mapped[int] = mapped_column(primary_key=True)
    ozon_sku: Mapped[str] = mapped_column(String) #Спарсенная таблица с озона и перелитая в нашу БД
    make: Mapped[str] = mapped_column(String) #Спарсенная таблица с озона и перелитая в нашу БД
    model: Mapped[str] = mapped_column(String) #Спарсенная таблица с озона и перелитая в нашу БД
    modification: Mapped[str] = mapped_column(String) #Спарсенная таблица с озона и перелитая в нашу БД
    
"""
Вся медия по товарам + сертификаты
"""
class Media(Base):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    image_1: Mapped[str] = mapped_column(String) #Ссылка на главное фото*
    image_2: Mapped[str] = mapped_column(String) #Ссылки на дополнительные фото
    image_3: Mapped[str] = mapped_column(String) #Ссылки на дополнительные фото
    image_4: Mapped[str] = mapped_column(String) #Ссылки на дополнительные фото
    image_5: Mapped[str] = mapped_column(String) #Ссылки на дополнительные фото
    image_6: Mapped[str] = mapped_column(String) #Ссылки на дополнительные фото
    image_7: Mapped[str] = mapped_column(String) #Ссылки на дополнительные фото
    image_8: Mapped[str] = mapped_column(String) #Ссылки на дополнительные фото
    image_9: Mapped[str] = mapped_column(String) #Ссылки на дополнительные фото
    image_10: Mapped[str] = mapped_column(String) #Ссылки на дополнительные фото
    rich: Mapped[str] = mapped_column(String) #Rich-контент JSON
    video: Mapped[str] = mapped_column(String) #только у Lynx и у суффикс 1 видео, формируется по формуле https://docs.google.com/spreadsheets/d/1vVZpcRGSD_45X2o2AfeQeWSTvIFrHGgrBTEd-hCWdmA/edit?gid=1972987555#gid=1972987555
    video_cover: Mapped[str] = mapped_column(String) #Видеообложки
    pdf_instruction: Mapped[str] = mapped_column(String) #Инструкция pdf
    certificate: Mapped[str] = mapped_column(String) #Сертификат соответствия (WB)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="media")

"""
Все, связанное с ценами
"""
class Price(Base):
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_price: Mapped[int] = mapped_column(Integer) #Закупочная цена
    price_ozon: Mapped[int] = mapped_column(Integer) #Моя цена, Формируется цена для озона, потом рассчитывается цена для WB/Yandex по чатботу
    profitability: Mapped[int] = mapped_column(Integer) #Рентабельность
    profit: Mapped[int] = mapped_column(Integer) #Прибыль, руб
    price: Mapped[int] = mapped_column(Integer) #Цена, руб.*
    price_before_discount: Mapped[int] = mapped_column(Integer) #Цена до скидки, руб, цена * 0,45
    vat: Mapped[int] = mapped_column(Integer) #НДС, %*, 20% 820 id, на wb нет ндс, на ян 1й магаз есть ндс 20
    products: Mapped[list["Product"]] = relationship("Product", back_populates="price")


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    aliases: Mapped[list["BrandAlias"]] = relationship(
        "BrandAlias",
        back_populates="brand",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    products: Mapped[list["Product"]] = relationship("Product", back_populates="brand")


class BrandAlias(Base):
    __tablename__ = "brand_aliases"
    __table_args__ = (
        UniqueConstraint("brand_id", "marketplace", "alias_name", name="uq_brand_alias"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=False)
    marketplace: Mapped[MarketplaceEnum] = mapped_column(nullable=False)
    alias_name: Mapped[str] = mapped_column(nullable=False)

    brand = relationship("Brand", back_populates="aliases")

# --- Product ORM ---
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=False)
    brand: Mapped["Brand"] = relationship("Brand", back_populates="products")

    used_sku: Mapped[str] = mapped_column(String, nullable=True)
    sku_1: Mapped[str] = mapped_column(String, nullable=True)
    sku_2: Mapped[str] = mapped_column(String, nullable=True)
    common_sku: Mapped[str] = mapped_column(String, nullable=True)
    part_number: Mapped[int] = mapped_column(Integer, nullable=True)
    ozon_sku: Mapped[str] = mapped_column(String, nullable=True)
    ozon_id: Mapped[int] = mapped_column(Integer, nullable=True)
    wb_id: Mapped[int] = mapped_column(Integer, nullable=True)
    yandex_id: Mapped[int] = mapped_column(Integer, nullable=True)
    id_1c: Mapped[int] = mapped_column(Integer, nullable=True)
    id_mp: Mapped[int] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    keywords: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)

    size_id: Mapped[int] = mapped_column(ForeignKey("characteristics.id"), nullable=True)
    size: Mapped["Characteristics"] = relationship("Characteristics", back_populates="products")

    price_id: Mapped[int] = mapped_column(ForeignKey("prices.id"), nullable=True)
    price: Mapped["Price"] = relationship("Price", back_populates="products")

    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"), nullable=True)
    media: Mapped["Media"] = relationship("Media", back_populates="products")

    fitment_id: Mapped[int] = mapped_column(ForeignKey("fitment.id"), nullable=True)
    fitment: Mapped["Fitment"] = relationship("Fitment", back_populates="products")

    type_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    category: Mapped["Category"] = relationship("Category", back_populates="products")

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
    yandex_category_id = mapped_column(ForeignKey("marketplace_categories.id"), nullable=True)
    
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")
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
    yandex_category = relationship(
        "MarketplaceCategory",
        foreign_keys=[yandex_category_id],
        lazy="joined"
    )