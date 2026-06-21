from __future__ import annotations

from math import sqrt
from typing import Any

import joblib
import numpy as np

from ..config import DEFAULT_CRASH_THRESHOLD, MODEL_PATH


def _build_features(sensor: dict[str, float]) -> np.ndarray:
    accel_x = float(sensor["accel_x"])
    accel_y = float(sensor["accel_y"])
    accel_z = float(sensor["accel_z"])
    speed = float(sensor["speed"])
    latitude = float(sensor["latitude"])
    longitude = float(sensor["longitude"])

    accel_magnitude = sqrt(accel_x ** 2 + accel_y ** 2 + accel_z ** 2)
    impact_delta = abs(accel_magnitude - 9.81)
    jerk_proxy = impact_delta * max(speed, 1.0)

    return np.array([[accel_magnitude, impact_delta, speed, jerk_proxy, latitude, longitude]], dtype=np.float64)


class CrashDetector:
    def __init__(self) -> None:
        self.model_bundle: dict[str, Any] | None = None
        self.threshold: float = DEFAULT_CRASH_THRESHOLD

    def load(self) -> None:
        if self.model_bundle is not None:
            return
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. Run ml_model/train.py first."
            )
        self.model_bundle = joblib.load(MODEL_PATH)
        self.threshold = float(self.model_bundle.get("threshold", DEFAULT_CRASH_THRESHOLD))

    def predict(self, sensor_payload: dict[str, float]) -> dict[str, float | bool]:
        self.load()
        assert self.model_bundle is not None

        model = self.model_bundle["model"]
        x = _build_features(sensor_payload)

        probability = float(model.predict_proba(x)[0][1])
        impact_delta = float(x[0][1])

        # False-positive guard: require probability, impact spike, and meaningful speed.
        is_crash = probability >= self.threshold and impact_delta >= 4.5 and float(x[0][2]) >= 12.0

        return {
            "is_crash": is_crash,
            "crash_probability": probability,
            "threshold": self.threshold,
        }
