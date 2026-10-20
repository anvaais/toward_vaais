import os
from pathlib import Path

from dotenv import load_dotenv

from app.providers.base import ExtractionProvider
from app.providers.fixture_loader import load_mock_fixtures
from app.providers.mock import MockProvider


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_provider() -> ExtractionProvider:
    # Environment variables already set by the process take precedence over .env.
    load_dotenv(PROJECT_ROOT / ".env", override=False)
    mode = os.getenv("PROVIDER_MODE", "mock").strip().lower()

    if mode == "mock":
        return MockProvider(load_mock_fixtures())

    if mode == "gemini":
        try:
            from app.providers.gemini import GeminiProvider
            return GeminiProvider(
                api_key=os.getenv("GEMINI_API_KEY", ""),
                model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            )
        except ImportError:
            raise ValueError("Install the google-genai SDK for gemini mode") from None

    raise ValueError("Unsupported PROVIDER_MODE; choose mock or gemini")
