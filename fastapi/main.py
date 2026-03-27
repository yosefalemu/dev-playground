from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.items import router as items_router
from basic import router as basic_router
from static import router as static_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(items_router)
app.include_router(basic_router)
app.include_router(static_router)



