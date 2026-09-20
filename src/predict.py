"""Bike demand prediction from user input."""

from pathlib import Path
import pickle

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "gradient_boosting_model.pkl"
SCALER_PATH = PROJECT_ROOT / "models" / "scaler.pkl"

NUMERIC_FEATURES = [
    "Hour",
    "Temperature(°C)",
    "Humidity(%)",
    "Wind speed (m/s)",
    "Visibility (10m)",
    "Solar Radiation (MJ/m2)",
    "Rainfall(mm)",
    "Snowfall (cm)",
]

FEATURE_ORDER = NUMERIC_FEATURES + [
    "is_peak_hour",
    "is_night",
    "is_working_day",
    "is_holiday",
    "season_Spring",
    "season_Summer",
    "season_Winter",
]

SEASONS = ["Spring", "Summer", "Autumn", "Winter"]


class InvalidInputError(ValueError):
    """Raised when user input fails validation."""


_model = None
_scaler = None


def _load():
    global _model, _scaler
    if _model is None:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
        with open(SCALER_PATH, "rb") as f:
            _scaler = pickle.load(f)
    return _model, _scaler


def validate(inputs: dict) -> None:
    """Check required fields are present and in range."""
    ranges = {
        "hour": (0, 23),
        "temperature": (-30, 45),
        "humidity": (0, 100),
        "wind_speed": (0, 30),
        "visibility": (0, 2000),
        "solar_radiation": (0, 5),
        "rainfall": (0, 100),
        "snowfall": (0, 30),
    }
    for field, (low, high) in ranges.items():
        value = inputs.get(field)
        if value is None:
            raise InvalidInputError(f"Missing required input: {field}")
        try:
            value = float(value)
        except (TypeError, ValueError) as exc:
            raise InvalidInputError(f"{field} must be a number, got {value}") from exc
        if not low <= value <= high:
            raise InvalidInputError(
                f"{field} must be between {low} and {high}, got {inputs.get(field)}"
            )
    if inputs.get("season") not in SEASONS:
        raise InvalidInputError(f"Season must be one of {SEASONS}")


def build_features(inputs: dict) -> pd.DataFrame:
    """Rebuild the engineered features the model was trained on."""
    hour = int(inputs["hour"])
    season = inputs["season"]

    # is_peak_hour: hours 18-22; is_night: hour < 6; Autumn is the dropped season.
    row = {
        "Hour": hour,
        "Temperature(°C)": inputs["temperature"],
        "Humidity(%)": inputs["humidity"],
        "Wind speed (m/s)": inputs["wind_speed"],
        "Visibility (10m)": inputs["visibility"],
        "Solar Radiation (MJ/m2)": inputs["solar_radiation"],
        "Rainfall(mm)": inputs["rainfall"],
        "Snowfall (cm)": inputs["snowfall"],
        "is_peak_hour": int(18 <= hour <= 22),
        "is_night": int(hour < 6),
        "is_working_day": int(inputs.get("functioning_day", True)),
        "is_holiday": int(inputs.get("is_holiday", False)),
        "season_Spring": int(season == "Spring"),
        "season_Summer": int(season == "Summer"),
        "season_Winter": int(season == "Winter"),
    }

    df = pd.DataFrame([row])[FEATURE_ORDER]
    _, scaler = _load()
    df[NUMERIC_FEATURES] = scaler.transform(df[NUMERIC_FEATURES])
    return df


def predict_demand(inputs: dict) -> int:
    """Return predicted bike rentals for the given conditions."""
    validate(inputs)
    model, _ = _load()
    features = build_features(inputs)
    prediction = model.predict(features)[0]
    return max(0, round(prediction))
