"""Local Ollama guidance for a bike-demand prediction."""

import os

import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
REQUEST_TIMEOUT_SECONDS = 20


def _build_prompt(prediction: int, inputs: dict) -> str:
    return (
        "You are assisting a bike-share operator.\n\n"
        "A machine learning model has already predicted hourly rental demand. "
        "Treat the predicted number as given. Do not calculate, estimate, "
        "recalculate, or second-guess the demand figure. Do not invent a "
        "different number.\n\n"
        f"Predicted bike rentals: {prediction}\n"
        "Input conditions:\n"
        f"- Hour: {inputs.get('hour')}\n"
        f"- Temperature (C): {inputs.get('temperature')}\n"
        f"- Humidity (%): {inputs.get('humidity')}\n"
        f"- Wind speed (m/s): {inputs.get('wind_speed')}\n"
        f"- Visibility (10m): {inputs.get('visibility')}\n"
        f"- Solar radiation (MJ/m2): {inputs.get('solar_radiation')}\n"
        f"- Rainfall (mm): {inputs.get('rainfall')}\n"
        f"- Snowfall (cm): {inputs.get('snowfall')}\n"
        f"- Season: {inputs.get('season')}\n"
        f"- Functioning day: {inputs.get('functioning_day')}\n"
        f"- Holiday: {inputs.get('is_holiday')}\n\n"
        "Write two or three sentences of operational guidance. Interpret the "
        "given prediction and conditions for staffing, bike availability, "
        "or station monitoring."
    )


def generate_guidance(prediction: int, inputs: dict) -> str | None:
    """Return operator guidance, or None if the local LLM is unavailable."""
    try:
        response = requests.post(
            f"{OLLAMA_URL.rstrip('/')}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": _build_prompt(prediction, inputs),
                "stream": False,
                "options": {"num_predict": 120},
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        text = response.json().get("response", "").strip()
        return text or None
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return None
