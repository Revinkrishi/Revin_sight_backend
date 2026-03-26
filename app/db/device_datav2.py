from pydantic import BaseModel
from typing import Optional, Dict, Union


class SensorData(BaseModel):
    median: Optional[float] = None
    mean: Optional[float] = None
    sd: Optional[float] = None


class DeviceDataV2(BaseModel):
    TIME: str
    DATE: str
    IMEI: str
    NWID: Optional[str] = None
    SIMNO: Optional[str] = None
    BATV: Optional[Union[str, float]] = None
    SOC: Optional[Union[str, int]] = None

    FWV: Optional[str] = None
    FWv: Optional[str] = None  # handle both

    LONG: Optional[Union[str, float]] = None
    LATT: Optional[Union[str, float]] = None

    # ✅ NEW FIELD
    Tamper: Optional[int] = None

    sensors: Dict[str, Union[float, SensorData]]

    API_KEY: Optional[str] = None