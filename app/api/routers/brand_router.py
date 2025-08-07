from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.di.dependencies import get_async_session, get_brand_matching_service
from app.api.services.brand_service import BrandMatchingService
from io import BytesIO

router = APIRouter()

@router.post("/brands/normalize-excel")
async def normalize_brands_excel(
    file: UploadFile = File(...),
    service: BrandMatchingService = Depends(get_brand_matching_service)
):
    content = await file.read()

    try:
        df = await service.canonicalize_brands_in_excel(content)
    except ValueError as e:
        return {"detail": str(e)}

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
