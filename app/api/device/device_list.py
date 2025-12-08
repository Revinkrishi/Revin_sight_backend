from fastapi import APIRouter, Depends, HTTPException, Query
from app.db.mongodb import get_db
from app.utils.sensor_mapper import map_sensor_names
from app.core.security import validate_query_api_key, verify_static_token
from datetime import datetime
import pytz

router = APIRouter()

@router.get("/device/all")
def list_all_device_data(
    auth=Depends(verify_static_token),
    api_key: str = Query(None)
):
    print("\n================ DEBUG LOG START ================", flush=True)

    # 1. Print API key received
    print(f"➡ Received api_key: {api_key}", flush=True)

    # 2. Validate API key (if provided)
    if api_key:
        try:
            validate_query_api_key(api_key)
            print("✔ API key validation PASSED", flush=True)
        except Exception as e:
            print(f"❌ API key validation FAILED: {str(e)}", flush=True)
            raise

    # 3. Connect to DB
    db = get_db()
    print("✔ Connected to MongoDB", flush=True)

    # 4. Build Mongo query
    query = {}
    if api_key:
        query["device.API_KEY"] = api_key

    print(f"➡ MongoDB Query Built: {query}", flush=True)

    # 5. Fetch data
    docs = list(db.device_data.find(query).sort("_id", -1))
    print(f"✔ Documents Found: {len(docs)}", flush=True)

    if len(docs) > 0:
        print(f"➡ First Document API_KEY: {docs[0]['device'].get('API_KEY')}", flush=True)
    else:
        print("❗ No documents matched the query", flush=True)

    # 6. Convert results
    results = []
    ist = pytz.timezone("Asia/Kolkata")

    for i, doc in enumerate(docs):
        print(f"➡ Processing Document #{i+1}", flush=True)

        utc_time = doc.get("received_at")
        if utc_time:
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ist)
            print(f"   ─ received_at (UTC): {utc_time}", flush=True)
            print(f"   ─ local_time (IST): {local_time}", flush=True)

        results.append({
            "device": doc.get("device", {}),
            "sensors": map_sensor_names(doc.get("sensors", {})),
            "received_at": local_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    print("================ DEBUG LOG END =================\n", flush=True)

    return results
