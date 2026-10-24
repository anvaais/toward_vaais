# VA-AIS Core

FastAPI service for extracting structured travel-lead information.

## Setup

Install the project and development dependencies declared in `pyproject.toml`:

```powershell
uv sync
```

## Run the API

Run from the `vaais-core` project directory:

```powershell
uv run uvicorn app.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs`.

## Run tests

```powershell
uv run pytest
```

The default provider is the offline mock. It returns fixture data for exact
matches in `data/fixtures.jsonl`; other inputs return unknown fields requiring
review.
## APIs 
we use the google apis