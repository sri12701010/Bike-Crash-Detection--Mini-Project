from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "backend"
ML_MODEL_DIR = BACKEND_DIR / "src" / "models"

MODEL_PATH = ML_MODEL_DIR / "crash_model.joblib"
PREDICTION_LOG_PATH = BACKEND_DIR / "logs" / "predictions.log"
SENSOR_INGEST_LOG_PATH = BACKEND_DIR / "logs" / "sensor_ingest.log"

DEFAULT_CRASH_THRESHOLD = 0.75
