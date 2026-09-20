# AI-Assisted Development Prompts

## Application Structure

Prompt used:

```
Suggest a simple Streamlit app structure that separates the UI,
the bike-demand prediction, and the local Ollama call.
```

What I used:

I used the three-file split: `app.py`, `src/predict.py`, and `src/llm_service.py`.

## ML Model Integration

Prompt used:

```
Help me load the Gradient Boosting pickle and make a prediction from
form inputs. The model was trained with scaled features.
```

What I used:

I kept the generated prediction function, then checked `prepare_data.py`
so peak hour, night, and season matching were the same as training.

## Local LLM Integration

Prompt used:

```
Help me send the prediction to the local Ollama service and get a short
explanation for a bike-share operator.
```

What I used:

I used the tutorial `/api/generate` call. I added a line in the prompt
telling the model not to recalculate the demand number.

## LLM Failure Handling

Prompt used:

```
If Ollama is unavailable, still show the ML prediction.
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
