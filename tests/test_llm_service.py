"""Failure-handling tests for the local LLM client."""

from src import llm_service


def test_generate_guidance_returns_none_when_ollama_unreachable(monkeypatch):
    monkeypatch.setattr(llm_service, "OLLAMA_URL", "http://127.0.0.1:9")
    monkeypatch.setattr(llm_service, "REQUEST_TIMEOUT_SECONDS", 1)

    result = llm_service.generate_guidance(
        742,
        {
            "hour": 18,
            "temperature": 25,
            "humidity": 50,
            "wind_speed": 2,
            "visibility": 2000,
            "solar_radiation": 0.5,
            "rainfall": 0,
            "snowfall": 0,
            "season": "Summer",
            "functioning_day": True,
            "is_holiday": False,
        },
    )

    assert result is None
