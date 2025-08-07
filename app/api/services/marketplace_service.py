import pandas as pd
from app.api.services.category_service import CategoryAttributesService

class MarketplaceService:
    def __init__(self, attr_service: CategoryAttributesService, category_repo):
        self.attr_service = attr_service
        self.category_repo = category_repo

    async def get_local_category_map(self):
        categories = await self.category_repo.get_all_local_categories_with_mp_ids()
        local_cat_map = {}
        for cat in categories:
            local_cat_map[cat.id] = {
                "ozon": cat.ozon_category.external_id if cat.ozon_category else None,
                "wb": cat.wb_category.external_id if cat.wb_category else None,
                # "yandex": cat.yandex_category.external_id if hasattr(cat, 'yandex_category') else None,
            }
        return local_cat_map

    async def get_templates(self) -> dict:
        local_cat_map = await self.get_local_category_map()
        templates = {"ozon": {}, "wb": {}, "yandex": {}}
        print("Local Category Map:", local_cat_map)
        for local_cat_id, mp_cats in local_cat_map.items():
            attrs = await self.attr_service.get_required_attributes(local_cat_id)
            for mp in templates.keys():
                cat_id = mp_cats.get(mp)
                if not cat_id:
                    continue
                mp_attrs = attrs.get(mp, {})
                required = [a["name"] for a in mp_attrs.get("required", [])]
                optional = [a["name"] for a in mp_attrs.get("optional", [])]
                # Без лишних полей
                templates[mp][cat_id] = {
                    "required": required,
                    "optional": optional,
                }

        return templates

    def split_file_on_marketplaces(self, df: pd.DataFrame, templates: dict, local_cat_map: dict, products: list) -> dict:
        result_files = {}

        base_columns = [
            "id", "brand_id", "used_sku", "sku_1", "sku_2", "common_sku", "part_number",
            "id_1c", "id_mp", "name", "description", "keywords", "created_at", "updated_at",
            "comment", "size_id", "price_id", "media_id", "fitment_id", "type_id"
        ]

        mp_own_fields = {
            "ozon": ["ozon_id", "ozon_sku"],
            "wb": ["wb_id", "wb_sku"],
            "yandex": ["yandex_id"]
        }

        other_id_cols = {
            "ozon": ["wb_id", "yandex_id", "wb_sku"],
            "wb": ["ozon_id", "yandex_id", "ozon_sku"],
            "yandex": ["ozon_id", "wb_id", "ozon_sku", "wb_sku"]
        }

        # Словарь с дополнительными данными по id
        product_data = {}


        for product in products:
            product_data[product.id] = {
                "Название модели": product.name,
                "Страна производства": product.size.country if product.size else None,
                "Комплектация": product.size.quantity_text if product.size else None,
                "Тип": product.category.name if product.category else None,
                "Ставка НДС": product.price.vat if product.price else None,
                "Бренд": product.brand.name if product.brand else None,
                "Партномер": product.common_sku or product.sku_1 or product.sku_2,
                "Номер сертификата": product.media.certificate if product.media else None,
                "Номер декларации соответствия": product.media.certificate if product.media else None,  # если всё в одном
            }

        for mp in ["ozon", "wb", "yandex"]:
            sku_col = f"{mp}_id"

            if sku_col not in df.columns:
                print(f"Skipped {mp}: no {sku_col} column")
                continue

            mp_rows = df[df[sku_col].notna()].copy()
            if mp_rows.empty:
                continue

            mp_final_df = pd.DataFrame()

            for local_cat_id in mp_rows["type_id"].unique():
                cat_id = local_cat_map.get(local_cat_id, {}).get(mp)
                if not cat_id:
                    print(f"Category not mapped for {mp}: {local_cat_id}")
                    continue

                if mp not in templates or cat_id not in templates[mp]:
                    print(f"No template for {mp} - category: {cat_id}")
                    continue

                template = templates[mp][cat_id]
                required = template.get("required", [])
                optional = template.get("optional", [])

                group = mp_rows[mp_rows["type_id"] == local_cat_id].copy()

                # Удаляем чужие колонки
                group = group.drop(columns=[col for col in other_id_cols[mp] if col in group.columns], errors="ignore")

                # Сохраняем свои поля
                own_fields = [col for col in mp_own_fields.get(mp, []) if col in df.columns]

                # Объединяем все поля, которые нужны для этой категории
                if mp == "wb":
                    optional_available = [col for col in optional if col in df.columns]
                    final_columns = base_columns + own_fields + required + optional_available
                else:
                    final_columns = base_columns + own_fields + required + optional

                final_columns = list(dict.fromkeys(final_columns))

                # Заполняем недостающие колонки из product_data
                for col in final_columns:
                    if col not in group.columns:
                        group[col] = ""

                for idx, row in group.iterrows():
                    pid = row["id"]
                    pdata = product_data.get(pid, {})
                    for field, value in pdata.items():
                        if field in final_columns:
                            group.at[idx, field] = value

                # Проверка обязательных полей для Ozon
                if mp == "ozon":
                    for req_field in required:
                        if group[req_field].isnull().all() or (group[req_field] == "").all():
                            print(f"[WARNING] Ozon: обязательное поле '{req_field}' пустое для категории {local_cat_id}")

                # Финальный DataFrame для этой группы
                group = group[final_columns]
                mp_final_df = pd.concat([mp_final_df, group], ignore_index=True)

            if not mp_final_df.empty:
                result_files[mp] = mp_final_df

        return result_files
