from typing import Optional
from fastapi import UploadFile
import pandas as pd
from io import BytesIO
from app.api.tasks.import_products import import_products_task
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.infrastructure.orm.models.product_orm import Product # пример, замените на свою модель
from sqlalchemy import select

class ProductExportService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def export_products_to_excel(self, category_id: Optional[int] = None) -> bytes:
        # Получить товары из БД (пример, замените на свою логику)
        query = select(Product)
        if category_id:
            query = query.where(Product.type_id == category_id)
        result = await self.session.execute(query)
        products = result.scalars().all()

        # Преобразовать в DataFrame
        data = [
            {
                "title": p.title,
                "ozon_sku": p.ozon_sku,
                "wb_sku": p.wb_sku,
                "brand": p.brand,
                "id_1c": p.id_1c,
                "multiplicity": p.multiplicity,
                "activity": p.activity,
                # добавьте нужные поля
            }
            for p in products
        ]
        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False)
        return output.getvalue()
    
class ProductImportService:
    async def start_import_task(self, file: UploadFile) -> str:
        content = await file.read()
        # Передать файл в Celery-задачу
        task = import_products_task.delay(content) # type: ignore
        return task.id