from fastapi import APIRouter, Depends, HTTPException, Query
from app.db.mongodb import get_db
from app.utils.sensor_mapper import map_sensor_names
from app.core.security import validate_query_api_key, verify_static_token
from datetime import datetime
import pytz

router = APIRouter()

"""code with issue of big data fetching in one calling"""

# @router.get("/device/all")
# def list_all_device_data(
#     auth=Depends(verify_static_token),
#     api_key: str = Query(None)
# ):
#     print("\n================ DEBUG LOG START ================", flush=True)

#     # 1. Print API key received
#     print(f"➡ Received api_key: {api_key}", flush=True)

#     # 2. Validate API key (if provided)
#     if api_key:
#         try:
#             validate_query_api_key(api_key)
#             print("✔ API key validation PASSED", flush=True)
#         except Exception as e:
#             print(f"❌ API key validation FAILED: {str(e)}", flush=True)
#             raise

#     # 3. Connect to DB
#     db = get_db()
#     print("✔ Connected to MongoDB", flush=True)

#     # 4. Build Mongo query
#     query = {}
#     if api_key:
#         query["device.API_KEY"] = api_key

#     print(f"➡ MongoDB Query Built: {query}", flush=True)

#     # 5. Fetch data
#     docs = list(db.device_data.find(query).sort("_id", -1))
#     print(f"✔ Documents Found: {len(docs)}", flush=True)

#     if len(docs) > 0:
#         print(f"➡ First Document API_KEY: {docs[0]['device'].get('API_KEY')}", flush=True)
#     else:
#         print("❗ No documents matched the query", flush=True)

#     # 6. Convert results
#     results = []
#     ist = pytz.timezone("Asia/Kolkata")

#     for i, doc in enumerate(docs):
#         print(f"➡ Processing Document #{i+1}", flush=True)

#         utc_time = doc.get("received_at")
#         if utc_time:
#             local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ist)
#             print(f"   ─ received_at (UTC): {utc_time}", flush=True)
#             print(f"   ─ local_time (IST): {local_time}", flush=True)

#         results.append({
#             "device": doc.get("device", {}),
#             "sensors": map_sensor_names(doc.get("sensors", {})),
#             "received_at": local_time.strftime("%Y-%m-%d %H:%M:%S")
#         })

#     print("================ DEBUG LOG END =================\n", flush=True)

#     return results

"""code with fetching device data with pagination and limit"""

@router.get("/device/all")
def list_all_device_data(
    auth=Depends(verify_static_token),
    api_key: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(500, le=1000)
):
    print("\n================ DEBUG LOG START ================", flush=True)

    print(f"➡ Received api_key: {api_key}", flush=True)
    print(f"➡ Page: {page}", flush=True)
    print(f"➡ Limit: {limit}", flush=True)

    # Validate API key
    if api_key:
        try:
            validate_query_api_key(api_key)
            print("✔ API key validation PASSED", flush=True)
        except Exception as e:
            print(f"❌ API key validation FAILED: {str(e)}", flush=True)
            raise

    # Connect DB
    db = get_db()
    print("✔ Connected to MongoDB", flush=True)

    # Build Query
    query = {}
    if api_key:
        query["device.API_KEY"] = api_key

    print(f"➡ MongoDB Query Built: {query}", flush=True)

    # Calculate Skip
    skip = (page - 1) * limit
    print(f"➡ Skip Value: {skip}", flush=True)

    # Get Total Count (for debugging)
    total_count = db.device_data.count_documents(query)
    print(f"✔ Total Matching Documents: {total_count}", flush=True)

    # Fetch Paginated Data
    cursor = (
        db.device_data
        .find(query)
        .sort("_id", -1)
        .skip(skip)
        .limit(limit)
    )

    ist = pytz.timezone("Asia/Kolkata")
    results = []
    processed_count = 0

    for doc in cursor:
        processed_count += 1
        print(f"➡ Processing Document #{processed_count}", flush=True)

        utc_time = doc.get("received_at")
        local_time = None

        if utc_time:
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ist)

        results.append({
            "device": doc.get("device", {}),
            "sensors": map_sensor_names(doc.get("sensors", {})),
            "received_at": local_time.strftime("%Y-%m-%d %H:%M:%S") if local_time else None
        })

    print(f"✔ Documents Returned This Page: {processed_count}", flush=True)
    print("================ DEBUG LOG END =================\n", flush=True)

    return {
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "returned_count": processed_count,
        "data": results
    }
