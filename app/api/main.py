from fastapi import FastAPI
from app.api.routers import category_router
from app.api.routers import product_router
from app.api.routers import brand_router
from app.api.routers import marketplace_router
app = FastAPI()

app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(brand_router.router)
app.include_router(marketplace_router.router)