# Vaais Day 7 — Provider Adapter

## Installation and safety

1. Back up or commit your existing work. This patch includes a replacement app/main.py; **review/diff it before overwriting**.
2. Copy `app/providers/*.py`, `tests/test_day7_providers.py`, and `.env.example` to your repository.
3. Use the included `app/main.py` as a reference for changing your existing endpoint; do not remove your earlier exercises.
4. Keep existing `app/schemas.py` and `data/fixtures.jsonl` (ten Day 5/6 fixtures). They are NOT included in this patch.
5. From project root: `uv pip install python-dotenv google-genai` (or use `uv add python-dotenv google-genai` if you use uv-managed pyproject.toml).
6. Check that `.gitignore` excludes `.env`, `.venv/`, `__pycache__/`, `.pytest_cache/`.
7. Copy the settings in `.env.example` to your existing `.env`. Don't commit real API keys.

## Validation

From project root:

- `uv run pytest tests/test_day7_providers.py -v` (11 checks)
- `uv run uvicorn app.main:app --reload`
- Open `/docs`; use existing case_001 text to test `POST /extract`.
- Switch `.env` to `PROVIDER_MODE=gemini` and provide `GEMINI_API_KEY` only if authorized and you accept potential billing.
- Restart the server and try the same request. **Live Gemini execution is optional.**
- To test failure without a valid key, use `PROVIDER_MODE=gemini`, `GEMINI_API_KEY=` (blank), restart and send POST /extract; expect a clear 503 response, not fabricated results.
- SDK version to record in README after installation (run locally): `uv run python -c "import importlib.metadata; print(importlib.metadata.version('google-genai'))"`
- To capture evidence: actual test output, API response, `git rev-parse --short HEAD` after commit, and configured model ID. No fake screenshot.

## Notes

- The offline mock returns labels only for **exact** Day 5/6 fixture texts; everything else returns the Day 6 unknown stub.
- The factory uses `PROVIDER_MODE` to select the provider. No hidden fallback after Gemini errors.
- Google SDK structured output validates shape, not semantic truth. Human review is still necessary for uncertain fields.
- `price` stores the amount only, not the currency. This is a known limitation of the existing schema.
- The existing tests that assume `/extract` always returns an unknown stub will need revision after connecting the mock; do not hide or delete failing tests.

## Short recall

- `base.py`: What every provider must return.
- `mock.py`: How offline expected labels are returned.
- `fixture_loader.py`: Converts existing JSONL into Pydantic objects.
- `gemini.py`: Calls real SDK and validates its output; external request may cost money.
- `factory.py`: Selects mock vs Gemini according to environment.
- `main.py`: Receives request, delegates to provider, returns response/error.

## Business requirement (manual verification)

I researched and placed three public tour-company leads in `docs/day7_prospects.csv`. Review them and copy them into your existing 15-prospect sheet. For each record, capture company name, buyer role (e.g. owner or operations manager; don't invent a named person), public contact path, and date verified. No particular contact person or buyer title has been verified. Do not send automatic outreach yet. Sample format:

| Company | Buyer role | Public contact path | Verified date |
| --- | --- | --- | --- |
| (research) | Owner / operations | Official contact page | YYYY-MM-DD |
| (research) | Operations manager | Official contact page | YYYY-MM-DD |
| (research) | Customer support lead | Official contact page | YYYY-MM-DD |
