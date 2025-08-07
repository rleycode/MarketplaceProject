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
                mp_attrs = attrs.get(mp, [])
                required = [a["name"] for a in mp_attrs if a.get("is_required", True)]
                optional = [a["name"] for a in mp_attrs if not a.get("is_required", True)]

                # Без лишних полей
                templates[mp][cat_id] = {
                    "required": required,
                    "optional": optional,
                }

        return templates

    def split_file_on_marketplaces(self, df: pd.DataFrame, templates: dict, local_cat_map: dict) -> dict:

        result_files = {}

        for mp in ["ozon", "wb", "yandex"]:
            sku_col = f"{mp}_id"
            other_id_cols = {"ozon": ["wb_id", "yandex_id"], "wb": ["ozon_id", "yandex_id"], "yandex": ["ozon_id", "wb_id"]}

            if sku_col not in df.columns:
                print(f"Skipped {mp}: no {sku_col} column")
                continue

            mp_rows = df[df[sku_col].notna()].copy()
            print(f"{mp}: rows with non-empty {sku_col}: {len(mp_rows)}")

            if mp_rows.empty:
                print(f"No data for {mp}")
                continue

            mp_final_df = pd.DataFrame()

            for local_cat_id in mp_rows["type_id"].unique():
                cat_id = local_cat_map.get(local_cat_id, {}).get(mp)
                print(f"Processing local_cat_id={local_cat_id} -> cat_id={cat_id} for {mp}")
                if not cat_id:
                    continue
                if mp not in templates or cat_id not in templates[mp]:
                    print(f"Template missing for cat_id={cat_id} in {mp}")
                    continue

                template = templates[mp][cat_id]
                required = template.get("required", [])
                optional = template.get("optional", [])

                group = mp_rows[mp_rows["type_id"] == local_cat_id].copy()

                # Удаляем другие ID
                for col in other_id_cols[mp]:
                    if col in group.columns:
                        group[col] = None

                # Добавим недостающие обязательные поля
                for col in required:
                    if col not in group.columns:
                        group[col] = ""

                mp_final_df = pd.concat([mp_final_df, group], ignore_index=True)

            if not mp_final_df.empty:
                result_files[mp] = mp_final_df
            else:
                print(f"No data collected for {mp}")

        return result_files
