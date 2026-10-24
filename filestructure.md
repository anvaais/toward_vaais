# VA-AIS Core File Structure

This document gives a quick overview of the `vaais-core` project and the
purpose of its main files and directories.

## Directory tree

```text
vaais-core/
├── README.md
├── pyproject.toml
├── uv.lock
├── filestructure.md
├── app/
│   ├── __init__.py
│   ├── day2_pydantic.py
│   ├── day3_fastapi_out_response.py
│   ├── main.py
│   ├── schemas.py
│   └── providers/
│       ├── base.py
│       └── mock.py
├── data/
│   └── fixtures.jsonl
├── docs/
│   ├── api_contract.md
│   └── requirements.md
├── src/
│   └── vaais_core/
│       └── __init__.py
└── tests/
    ├── __init__.py
    ├── extraction_test.py
    ├── test_extract.py
    ├── test_fixture.py
    ├── test_health.py
    └── test_mock_provider.py
```

## File and directory descriptions

### Project root

- **`README.md`** — Main project introduction and usage documentation. It is
  documents setup, running the API, and running tests.
- **`pyproject.toml`** — Project metadata, Python version requirement,
  runtime dependencies, development dependencies, build configuration, and
  the `vaais-core` command-line entry point.
- **`uv.lock`** — Locked versions and dependency resolution data generated for
  the `uv` package manager.
- **`filestructure.md`** — This document; it explains the project layout.

### `app/`

The main application package. It contains the FastAPI application, Pydantic
schemas, provider abstractions, and prototype examples.

- **`app/__init__.py`** — Marks `app` as a Python package. It is currently
  empty.
- **`app/main.py`** — Defines the active FastAPI application, the `GET
  /health` endpoint, and the `POST /extract` endpoint. The extraction
  endpoint delegates to the configured extraction provider and returns
  fixture-backed results in mock mode.
- **`app/schemas.py`** — Defines the request and response models used by the
  API:
  `ExtractRequest`, `LeadFields`, and `ExtractionResponse`.
- **`app/day2_pydantic.py`** — Earlier Pydantic model prototype showing request
  validation and the lead response shape.
- **`app/day3_fastapi_out_response.py`** — Earlier FastAPI response-model
  prototype with a sample extraction response.

### `app/providers/`

Provider interfaces and implementations used to separate extraction logic from
the API layer.

- **`app/providers/base.py`** — Defines the `ExtractionProvider` protocol and
  the `ProviderError` exception.
- **`app/providers/mock.py`** — Implements `MockProvider`, which returns
  fixture-based responses when an input matches and otherwise returns a
  review-required fallback response.
- **`app/providers/factory.py`** — Loads provider configuration and selects the
  mock or Gemini provider.
- **`app/providers/fixture_loader.py`** — Loads and validates extraction
  fixtures from `data/fixtures.jsonl`.
- **`app/providers/gemini.py`** — Calls Gemini for structured extraction and
  validates the returned data.

### `data/`

Input data used by tests and development.

- **`data/fixtures.jsonl`** — Ten JSON Lines fixture cases covering clear,
  missing, ambiguous, contradictory, and form-derived travel requests. Each
  case includes input text and the expected extracted fields.

### `docs/`

Project requirements and API behavior documentation.

- **`docs/requirements.md`** — Defines the travel-lead extraction
  requirements, validation rules, non-goals, constraints, and acceptance
  criteria.
- **`docs/api_contract.md`** — Documents the `ExtractRequest` input contract
  and examples covering complete, incomplete, ambiguous, and contradictory
  travel requests.

### `src/vaais_core/`

The installable Python package configured by the project build settings.

- **`src/vaais_core/__init__.py`** — Package entry point containing the
  `main()` function used by the `vaais-core` console script.

### `tests/`

Automated tests for the API, schemas, fixtures, and provider behavior.

- **`tests/__init__.py`** — Marks `tests` as a Python package. It is currently
  empty.
- **`tests/test_health.py`** — Contains a basic health-check prototype test.
- **`tests/test_extract.py`** — Tests the active health and extraction
  endpoints, including request validation and malformed JSON handling.
- **`tests/test_fixture.py`** — Loads and validates all JSONL fixtures and
  verifies the API returns the matching fixture labels in mock mode.
- **`tests/test_mock_provider.py`** — Tests the mock extraction provider's
  fixture lookup, deep-copy behavior, and fallback response.
- **`tests/extraction_test.py`** — Standalone FastAPI health-check prototype
  used during early experimentation.
- **`tests/test_day7_providers.py`** — Tests provider selection, mock fixture
  behavior, and safe Gemini failure handling.
