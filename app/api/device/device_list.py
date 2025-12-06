from fastapi import APIRouter, Depends, HTTPException
from app.db.mongodb import get_db
from app.utils.sensor_mapper import map_sensor_names
from app.core.security import verify_static_token
from datetime import datetime
import pytz

router = APIRouter()

@router.get("/device/all")
def list_all_device_data(
    auth=Depends(verify_static_token)   # <-- HEADER TOKEN AUTH
):
    db = get_db()

    # Fetch all documents
    docs = db.device_data.find().sort("_id", -1)

    results = []
    ist = pytz.timezone("Asia/Kolkata")

    for doc in docs:
        raw_sensors = doc.get("sensors", {})
        mapped_sensors = map_sensor_names(raw_sensors)

        utc_time = doc.get("received_at")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ist)

        results.append({
            "device": doc.get("device", {}),
            "sensors": mapped_sensors,
            "received_at": local_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    return results
