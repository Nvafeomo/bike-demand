# Seoul Bike Demand

This Streamlit app predicts hourly bike rentals from weather and calendar
inputs. It uses the Gradient Boosting model from the Module 3 tutorial, then
sends that prediction to a local LLM for a short explanation.

User Input → ML Prediction → Local LLM → Explanation / Recommendation

The model files are in `models/`:

- `gradient_boosting_model.pkl`
- `scaler.pkl`

## Install Python packages

```powershell
python -m pip install -r requirements.txt
```

## Start the local LLM

Make sure Docker Desktop is running, then from this folder:

```powershell
docker compose up -d
docker exec sweng889-ollama ollama pull llama3.2:1b
```

The first pull can take a few minutes. To stop it later:

```powershell
docker compose down
```

## Run the application

```powershell
streamlit run app.py
```

Open the URL in the terminal (usually `http://localhost:8501`), fill in the
form, and click **Predict demand**.

## LLM-enabled capability

After the ML prediction is shown, the local LLM writes a short recommendation
for a bike-share operator. It explains the predicted demand using the input
conditions. It does not calculate the number itself.

If Ollama is not running, the prediction still shows and the guidance section
says the LLM is unavailable.

## Requirements

R1. Machine learning prediction
Validation: normal operation
Evidence: valid input produces an hourly rental prediction
Result: Pass

R2. Local LLM capability
Validation: normal operation
Evidence: the LLM writes a short recommendation based on the prediction
Result: Pass

R3. Failure handling
Validation: invalid input and LLM unavailable
Evidence: hour 47 shows an error message; the prediction still appears when Ollama is stopped
Result: Pass

R4. Separation of responsibilities
Validation: project structure
Evidence: UI is in `app.py`, prediction is in `src/predict.py`, Ollama is in `src/llm_service.py`
Result: Pass
