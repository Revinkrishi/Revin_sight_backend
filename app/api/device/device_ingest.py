from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from app.db.mongodb import get_db
from app.db.device_data import DeviceData
from app.core.security import validate_query_api_key  # <-- REUSE SAME VALIDATOR

router = APIRouter()

@router.post("/ingest")
async def ingest_data(request: Request):
    payload = await request.json()

    # Validate Pydantic model
    data = DeviceData(**payload)

    # -----------------------------------------
    # 1. Validate API_KEY exactly like GET API
    # -----------------------------------------
    validate_query_api_key(data.API_KEY)

    # -----------------------------------------
    # 2. Insert only if API_KEY is valid
    # -----------------------------------------
    db = get_db()
    db.device_data.insert_one({
        "device": {
            "TIME": data.TIME,
            "DATE": data.DATE,
            "IMEI": data.IMEI,
            "NWID": data.NWID,
            "SIMNO": data.SIMNO,    
            "BATV": data.BATV,
            "SOC": data.SOC,
            "FWv": data.FWv,
            "LONG": data.LONG,
            "LATT": data.LATT,
            "API_KEY": data.API_KEY,
        },
        "sensors": data.sensors,
        "received_at": datetime.utcnow()
    })

    return {"status": "OK"}
