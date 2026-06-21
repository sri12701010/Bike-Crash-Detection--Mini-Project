from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import PREDICTION_LOG_PATH, SENSOR_INGEST_LOG_PATH
from .inference.detect_crash import CrashDetector
from .schemas import AlertRequest, AlertResponse, PredictResponse, SensorData, UploadResponse
from .utils.alerts import simulate_alert
from .utils.logger import append_json_line

app = FastAPI(title="Bike Crash Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = CrashDetector()
sensor_buffer: list[dict] = []


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/sensor/upload", response_model=UploadResponse)
def upload_sensor_data(payload: SensorData) -> UploadResponse:
    sample_id = str(uuid4())
    data = payload.model_dump(mode="json")
    data["sample_id"] = sample_id

    sensor_buffer.append(data)
    append_json_line(SENSOR_INGEST_LOG_PATH, data)

    return UploadResponse(message="Sensor data stored successfully", sample_id=sample_id)


@app.post("/api/predict", response_model=PredictResponse)
def predict_crash(payload: SensorData) -> PredictResponse:
    sensor_data = payload.model_dump(mode="json")
    prediction = detector.predict(sensor_data)

    alert_triggered = False
    message = "No crash detected"

    if prediction["is_crash"]:
        alert_message = simulate_alert(
            latitude=payload.latitude,
            longitude=payload.longitude,
            contact="+1234567890",
            note="Crash detected by ML model",
        )
        alert_triggered = True
        message = alert_message

    append_json_line(
        PREDICTION_LOG_PATH,
        {
            "sensor": sensor_data,
            "prediction": prediction,
            "alert_triggered": alert_triggered,
        },
    )

    return PredictResponse(
        is_crash=bool(prediction["is_crash"]),
        crash_probability=float(prediction["crash_probability"]),
        threshold=float(prediction["threshold"]),
        alert_triggered=alert_triggered,
        message=message,
    )


@app.post("/api/alert", response_model=AlertResponse)
def send_manual_alert(payload: AlertRequest) -> AlertResponse:
    message = simulate_alert(
        latitude=payload.latitude,
        longitude=payload.longitude,
        contact=payload.contact,
        note=payload.note,
    )
    return AlertResponse(sent=True, message=message)


@app.get("/api/sensor/recent")
def recent_sensor_data(limit: int = 10) -> dict[str, list[dict]]:
    return {"items": sensor_buffer[-limit:]}
