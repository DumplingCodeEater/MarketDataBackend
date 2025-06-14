from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Market Data Service")

app.include_router(router, prefix="/prices")
