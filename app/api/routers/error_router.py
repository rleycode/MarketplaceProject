from fastapi import APIRouter, Depends

router = APIRouter(prefix="/errors", tags=["Errors"])

@router.get("/import/status/{task_id}")
async def get_import_status(task_id: str):
    # Получить статус из Celery или из БД
    # Вернуть прогресс и ошибки
    return {"status": "in_progress", "progress": 50, "errors": []}