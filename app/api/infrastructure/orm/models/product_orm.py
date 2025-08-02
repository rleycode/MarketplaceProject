from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.api.infrastructure.orm.database import Base

class Product(Base):
    __tablename__ = "nomenklatura"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str] = mapped_column(String, ForeignKey("brendy.name"))
    used_sku: Mapped[str] = mapped_column(String)
    sku_1: Mapped[str] = mapped_column(String)
    sku_2: Mapped[str] = mapped_column(String)
    common_sku: Mapped[str] = mapped_column(String)
    ozon_sku: Mapped[str] = mapped_column(String)
    part_number: Mapped[str] = mapped_column(String)
    id_1c: Mapped[str] = mapped_column(String)
    id_mp: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)
    wb_sku: Mapped[str] = mapped_column(String)
    ozon_update: Mapped[DateTime] = mapped_column(DateTime)
    wb_update: Mapped[DateTime] = mapped_column(DateTime)
    multiplicity: Mapped[int] = mapped_column(Integer)
    activity: Mapped[bool] = mapped_column(Boolean)
    comment: Mapped[str] = mapped_column(String)
    media_id: Mapped[int] = mapped_column(Integer, ForeignKey("media.id"))
    fitment_id: Mapped[int] = mapped_column(Integer, ForeignKey("fitment_-_primenyaemost.id"))
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey("kategorii_mp.id"))

    # Relationships
    brand_rel = relationship("Brand", back_populates="products", primaryjoin="Product.brand==Brand.name")
    media = relationship("Media", back_populates="products")
    fitment = relationship("Fitment", back_populates="products")
    category = relationship("MarketplaceCategory", back_populates="products")

# Пример моделей для связанных таблиц (минимально для связей):

class Brand(Base):
    __tablename__ = "brendy"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    # ... другие поля ...
    products = relationship("Product", back_populates="brand_rel")

class Media(Base):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # ... другие поля ...
    products = relationship("Product", back_populates="media")

class Fitment(Base):
    __tablename__ = "fitment_-_primenyaemost"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # ... другие поля ...
    products = relationship("Product", back_populates="fitment")

class MarketplaceCategory(Base):
    __tablename__ = "kategorii_mp"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # ... другие поля ...
    products = relationship("Product", back_populates="category")