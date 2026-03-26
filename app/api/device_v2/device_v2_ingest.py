from app.db.device_datav2 import DeviceDataV2
from datetime import datetime
from app.db.mongodb import get_db
from app.db.device_data import DeviceData
from app.core.security import validate_query_api_key  # <-- REUSE SAME VALIDATOR
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.post("/ingest/v2")
async def ingest_data(request: Request):
    payload = await request.json()

    # ✅ Use new model
    data = DeviceDataV2(**payload)

    validate_query_api_key(data.API_KEY)

    db = get_db()

    # ✅ Normalize sensors (handle old + new)
    normalized_sensors = {}

    for key, value in data.sensors.items():
        if isinstance(value, (int, float)):
            normalized_sensors[key] = {
                "name": None,
                "median": value,
                "mean": value,
                "sd": 0
            }
        else:
            normalized_sensors[key] = value.dict()

    db.device_data_v2.insert_one({
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
            "Tamper": data.Tamper
        },
        "sensors": normalized_sensors,  # ✅ always clean format
        "received_at": datetime.utcnow()
    })

    return {"status": "OK"}