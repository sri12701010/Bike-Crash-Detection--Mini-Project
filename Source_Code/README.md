# Bike Crash Detection System (End-to-End)

This repository contains a complete beginner-friendly Bike Crash Detection System with:

- Machine learning model training on synthetic sensor data.
- FastAPI backend for sensor upload, crash prediction, and alert simulation.
- React frontend for dashboard, sensor simulation form, and crash alert display.

## Project Structure

```text
backend/
  requirements.txt
  logs/
  src/
    app.py
    config.py
    schemas.py
    inference/
      detect_crash.py
    utils/
      alerts.py
      logger.py

frontend/
  package.json
  vite.config.js
  index.html
  src/
    App.jsx
    api.js
    styles.css
    components/
      Dashboard.jsx
      SensorForm.jsx
      AlertCard.jsx

ml_model/
  requirements.txt
  generate_dataset.py
  train.py
  detect_crash.py
  data/
  models/
```

## Features Implemented

1. Crash classification using sensor inputs:
   - accelerometer x/y/z
   - speed
   - GPS coordinates
2. REST APIs (FastAPI):
   - Upload sensor data
   - Predict crash
   - Send alert (simulated)
3. Pydantic request and response schemas.
4. CORS enabled for frontend communication.
5. Prediction logging and sensor ingest logging.
6. False-positive handling with threshold and impact checks.
7. Synthetic dataset generator.

## Setup and Run

### 1) ML Model Setup and Training

From repository root:

```bash
python -m venv .venv_ml
.venv_ml\Scripts\activate
pip install -r ml_model/requirements.txt
python ml_model/generate_dataset.py
python ml_model/train.py
```

This creates:

- ml_model/data/sensor_crash_dataset.csv
- backend/src/models/crash_model.joblib

### 2) Backend (FastAPI)

```bash
python -m venv .venv_backend
.venv_backend\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.src.app:app --reload --host 0.0.0.0 --port 8000
```

API base URL:

- http://127.0.0.1:8000/api

If port 8000 is busy, run on 8001:

```bash
uvicorn backend.src.app:app --reload --host 0.0.0.0 --port 8001
```

And set frontend API URL in frontend/.env:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8001/api
```

Useful endpoints:

- GET /api/health
- POST /api/sensor/upload
- POST /api/predict
- POST /api/alert
- GET /api/sensor/recent

### 3) Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

- http://127.0.0.1:5173

## Sample Predict Payload

```json
{
  "accel_x": 17.2,
  "accel_y": 1.9,
  "accel_z": 25.0,
  "speed": 44.5,
  "latitude": 12.9352,
  "longitude": 77.6245,
  "timestamp": "2026-04-01T10:00:00Z"
}
```

## Alert System

Alerts are simulated and include location data. The backend prints messages like:

```text
[ALERT] <timestamp> | Contact: +1234567890 | Location: (<lat>, <lon>) | Note: Crash detected by ML model
```

## Notes for Beginners

1. Train the model before starting backend prediction calls.
2. If model file is missing, backend predict endpoint returns model-not-found error.
3. You can tune threshold in:
   - ml_model/train.py (saved threshold)
   - backend/src/inference/detect_crash.py (additional false-positive guard)
