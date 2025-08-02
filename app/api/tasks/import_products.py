from celery import shared_task
import pandas as pd
from io import BytesIO

@shared_task(bind=True)
def import_products_task(self, file_bytes: bytes):
    errors = []
    imported = 0
    try:
        df = pd.read_excel(BytesIO(file_bytes))
        total = len(df)
        for idx, (_, row) in enumerate(df.iterrows()):
            self.update_state(state='PROGRESS', meta={'current': idx + 1, 'total': total})
            try:
                # Пример валидации обязательных полей
                required_fields = ["title", "ozon_sku", "wb_sku", "brand"]
                for field in required_fields:
                    if pd.isna(row.get(field)):
                        raise ValueError(f"Обязательное поле '{field}' не заполнено (строка {idx + 2})")

                # TODO: здесь логика создания/обновления товара в БД или через API МП
                # Например:
                # product = Product.get_or_create(...)
                # product.title = row["title"]
                # product.ozon_sku = row["ozon_sku"]
                # ...
                # product.save()

                imported += 1

            except Exception as row_exc:
                errors.append({"row": idx + 2, "error": str(row_exc)})

        return {
            "status": "completed",
            "total": total,
            "imported": imported,
            "errors": errors
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "errors": errors}