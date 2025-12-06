from fastapi import APIRouter, Query, HTTPException
from app.db.mongodb import get_db
from app.utils.sensor_mapper import map_sensor_names
from app.core.security import validate_query_api_key
from datetime import datetime
import pytz

router = APIRouter()

@router.get("/device")
def get_device_data(
    imei: str = Query(None),
    api_key: str = Query(None)
):
    db = get_db()

    # ---------------------
    # 1. VALIDATE API KEY
    # ---------------------
    if api_key:
        validate_query_api_key(api_key)

    # ---------------------
    # 2. BUILD QUERY
    # ---------------------
    query = {}

    if imei:
        query["device.IMEI"] = imei

    if api_key:
        query["device.API_KEY"] = api_key  # restrict to matching devices

    if not query:
        raise HTTPException(status_code=400, detail="IMEI or API_KEY required")

    # ---------------------
    # 3. FETCH ALL DATA
    # ---------------------
    docs = db.device_data.find(query).sort("_id", -1)

    results = []
    ist = pytz.timezone("Asia/Kolkata")

    for doc in docs:
        raw_sensors = doc.get("sensors", {})
        mapped_sensors = map_sensor_names(raw_sensors)

        utc_time = doc["received_at"]
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ist)

        results.append({
            "device": doc["device"],
            "raw_sensors": raw_sensors,
            "mapped_sensors": mapped_sensors,
            "received_at": local_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    if not results:
        raise HTTPException(status_code=404, detail="No data found")

    return results
