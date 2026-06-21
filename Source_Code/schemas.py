from datetime import datetime
from pydantic import BaseModel, Field


class SensorData(BaseModel):
    accel_x: float = Field(..., description="Acceleration X-axis in m/s^2")
    accel_y: float = Field(..., description="Acceleration Y-axis in m/s^2")
    accel_z: float = Field(..., description="Acceleration Z-axis in m/s^2")
    speed: float = Field(..., ge=0, description="Bike speed in km/h")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timestamp: datetime | None = Field(default=None)


class UploadResponse(BaseModel):
    message: str
    sample_id: str


class PredictResponse(BaseModel):
    is_crash: bool
    crash_probability: float
    threshold: float
    alert_triggered: bool
    message: str


class AlertRequest(BaseModel):
    latitude: float
    longitude: float
    contact: str = Field(default="+0000000000")
    note: str = Field(default="Potential bike crash detected")


class AlertResponse(BaseModel):
    sent: bool
    message: str
