# AI-Assisted Development Prompts

## Application Structure

Prompt used:

```
I need to build a small Streamlit app for my SWENG 889 assignment.
It should take weather and calendar inputs, predict hourly bike demand
with the Gradient Boosting model from the module 3 tutorial, then send
that prediction to the local Ollama LLM for a short recommendation.
Keep it simple. Separate the UI, the prediction code, and the Ollama
call into different files.
```

What I used:

I used the three-file split: `app.py`, `src/predict.py`, and `src/llm_service.py`.

## ML Model Integration

Prompt used:

```
Help me write predict.py. I have gradient_boosting_model.pkl and
scaler.pkl. The model was trained on scaled features, so I have to
rebuild the same columns from the form. Peak hour is 18-22, night is
hour under 6, and Autumn is the dropped season. Also check that the
inputs are in range before predicting.
```

What I used:

I kept the generated prediction function, then checked `prepare_data.py`
so peak hour, night, and season matching were the same as training.

## Local LLM Integration

Prompt used:

```
The prediction should go to the local Ollama service from the tutorial
(localhost:11434). I want a couple sentences of guidance for a bike
share operator. The LLM should use the number from the model. Do not
let it come up with its own demand estimate.
```

What I used:

I used the tutorial `/api/generate` call. I added a line in the prompt
telling the model not to recalculate the demand number.

## LLM Failure Handling

Prompt used:

```
If Ollama is down or the request fails, still show the ML prediction.
Also show a clear error if the user enters something invalid, like
hour 47. Do not crash the app.
```

What I used:

I used the try/except idea and a fallback message in the UI. I also added
a timeout because the first version hung when the container was stopped.

## Assignment Check

Prompt used:

```
Here is the assignment. Check that I am not missing anything and that
the README and PROMPT.md look complete.
```

What I used:

I used this as a final check. The app was already built. It mainly
confirmed the README and PROMPT.md covered what the assignment asked for.
