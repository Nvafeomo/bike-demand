"""Streamlit UI for bike-demand prediction and local LLM guidance."""

import streamlit as st

from src.llm_service import generate_guidance
from src.predict import InvalidInputError, predict_demand

st.set_page_config(page_title="Seoul Bike Demand", page_icon="🚲", layout="centered")

st.title("Seoul Bike Demand")
st.write(
    "Enter weather and calendar conditions to estimate hourly bike rentals. "
    "A local LLM then adds short operational guidance. The model does not "
    "recalculate the prediction."
)

with st.form("demand_form"):
    col1, col2 = st.columns(2)
    with col1:
        hour_raw = st.text_input("Hour (0-23)", value="18")
        temperature = st.number_input("Temperature (°C)", value=25.0, step=0.5)
        humidity = st.number_input("Humidity (%)", value=50.0, step=1.0)
        wind_speed = st.number_input("Wind speed (m/s)", value=2.0, step=0.1)
        visibility = st.number_input("Visibility (10m)", value=2000.0, step=10.0)
    with col2:
        solar_radiation = st.number_input(
            "Solar radiation (MJ/m2)", value=0.5, step=0.1
        )
        rainfall = st.number_input("Rainfall (mm)", value=0.0, step=0.1)
        snowfall = st.number_input("Snowfall (cm)", value=0.0, step=0.1)
        season = st.selectbox(
            "Season", ["Spring", "Summer", "Autumn", "Winter"], index=1
        )
        functioning_day = st.checkbox("Functioning day", value=True)
        is_holiday = st.checkbox("Holiday", value=False)

    submitted = st.form_submit_button("Predict demand")

if submitted:
    try:
        hour = int(hour_raw.strip()) if str(hour_raw).strip() != "" else None
    except ValueError:
        hour = hour_raw

    inputs = {
        "hour": hour,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "visibility": visibility,
        "solar_radiation": solar_radiation,
        "rainfall": rainfall,
        "snowfall": snowfall,
        "season": season,
        "functioning_day": functioning_day,
        "is_holiday": is_holiday,
    }

    try:
        prediction = predict_demand(inputs)
    except InvalidInputError as exc:
        st.error(str(exc))
    else:
        st.subheader("Predicted bike demand")
        st.metric("Hourly rentals", f"{prediction:,}")

        guidance = generate_guidance(prediction, inputs)
        st.subheader("AI-generated guidance")
        if guidance:
            st.write(guidance)
        else:
            st.warning(
                "AI guidance unavailable. The local LLM did not respond, "
                "but the machine learning prediction above is still valid."
            )
