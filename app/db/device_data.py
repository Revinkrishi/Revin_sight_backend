from pydantic import BaseModel
from typing import Optional, Dict

class DeviceData(BaseModel):
    # Device info
    TIME: str
    DATE: str
    IMEI: str
    NWID: Optional[str] = None
    SIMNO: Optional[str] = None   # <-- NEW FIELD ADDED
    BATV: Optional[str] = None    # keep as string since device sends string
    SOC: Optional[str] = None     # keep as string
    FWv: Optional[str] = None

    # GPS info
    LONG: Optional[str] = None
    LATT: Optional[str] = None

    # Raw sensors
    sensors: Dict[str, float]

    # API key
    API_KEY: Optional[str] = None
