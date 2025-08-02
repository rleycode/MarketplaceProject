from typing import Optional
from fastapi import UploadFile
import pandas as pd
from io import BytesIO
from app.api.tasks.import_products import import_products_task
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.infrastructure.orm.models.product_orm import Product
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class ProductExportService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def export_products_to_excel(self, category_id: Optional[int] = None) -> bytes:
        query = select(Product).options(
            selectinload(Product.media),
            selectinload(Product.fitment),
            selectinload(Product.category),
            selectinload(Product.brand_rel)
        )
        if category_id:
            query = query.where(Product.type_id == category_id)

        result = await self.session.execute(query)
        products = result.scalars().all()

        data = []
        for p in products:
            data.append({
                "Название": p.name,
                "Заголовок": p.title,
                "Бренд": p.brand,
                "Бренд (объект)": p.brand_rel.name if p.brand_rel else None,
                "SKU Ozon": p.ozon_sku,
                "SKU WB": p.wb_sku,
                "SKU общее": p.common_sku,
                "Part Number": p.part_number,
                "ID 1C": p.id_1c,
                "ID MP": p.id_mp,
                "Мультипликатор": p.multiplicity,
                "Активность": p.activity,
                "Комментарий": p.comment,
                "Обновлено Ozon": p.ozon_update,
                "Обновлено WB": p.wb_update,
                "Категория": p.category.name if p.category else None,
                "Медиа ID": p.media.id if p.media else None,
                "Применяемость": p.fitment.name if p.fitment else None,
            })

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False)
        return output.getvalue()
    
class ProductImportService:
    async def start_import_task(self, file: UploadFile) -> str:
        content = await file.read()
        task = import_products_task.delay(content)  # type: ignore
        return task.id