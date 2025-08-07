from io import BytesIO
import zipfile
from fastapi import APIRouter, Depends, File, Response, UploadFile
import pandas as pd

from app.api.di.dependencies import get_marketplace_service
from app.api.services.marketplace_service import MarketplaceService

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])

@router.post("/split", summary="Разделение общего файла по маркетплейсам")
async def split_marketplace_file(
    file: UploadFile = File(...),
    marketplace_service: MarketplaceService = Depends(get_marketplace_service),
):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))

    templates = await marketplace_service.get_templates()
    local_cat_map = await marketplace_service.get_local_category_map()

    split_files = marketplace_service.split_file_on_marketplaces(df, templates, local_cat_map)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for mp, mp_df in split_files.items():
            excel_buf = BytesIO()
            mp_df.to_excel(excel_buf, index=False)
            excel_buf.seek(0)
            zipf.writestr(f"{mp}_filtered.xlsx", excel_buf.read())

    zip_buffer.seek(0)

    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=split_files.zip"},
    )