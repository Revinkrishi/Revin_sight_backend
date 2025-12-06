from fastapi import FastAPI
from app.api.device.device_ingest import router as ingest_router
from app.api.device.device_fetch import router as fetch_router
from app.api.device.device_list import router as fetch_router

app = FastAPI(title="IoT Backend")

app.include_router(ingest_router, prefix="/api")
app.include_router(fetch_router, prefix="/api")
app.include_router(fetch_router, prefix="/api")
