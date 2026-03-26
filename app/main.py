from fastapi import FastAPI
from app.api.device.device_ingest import router as ingest_router
from app.api.device.device_fetch import router as fetch_router
from app.api.device.device_list import router as list_router
from app.api.device_v2.device_v2_ingest import router as ingest_router_v2
from app.api.device_v2.device_v2_list import router as list_router_v2

app = FastAPI(title="IoT Backend")

# device version 1
app.include_router(ingest_router, prefix="/api")
app.include_router(fetch_router, prefix="/api")
app.include_router(list_router, prefix="/api")

# device version 2
app.include_router(ingest_router_v2, prefix="/api")
app.include_router(list_router_v2, prefix="/api")

