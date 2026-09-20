"""Validation tests for bike-demand input handling."""

import pytest

from src.predict import InvalidInputError, validate

VALID_INPUTS = {
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
}


def test_validate_accepts_complete_in_range_input():
    validate(VALID_INPUTS)


def test_validate_rejects_missing_hour():
    inputs = dict(VALID_INPUTS)
    inputs["hour"] = None
    with pytest.raises(InvalidInputError, match="Missing required input: hour"):
        validate(inputs)


def test_validate_rejects_out_of_range_hour():
    inputs = dict(VALID_INPUTS)
    inputs["hour"] = 47
    with pytest.raises(InvalidInputError, match="hour must be between 0 and 23"):
        validate(inputs)


def test_validate_rejects_invalid_season():
    inputs = dict(VALID_INPUTS)
    inputs["season"] = "Fall"
    with pytest.raises(InvalidInputError, match="Season must be one of"):
        validate(inputs)
