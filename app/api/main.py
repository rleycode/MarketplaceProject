from fastapi import FastAPI
from app.api.routers import category_router
from app.api.routers import product_router
app = FastAPI()

app.include_router(category_router.router)
app.include_router(product_router.router)