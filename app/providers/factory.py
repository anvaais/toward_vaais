
from app.providers.base import ExtractionProvider
from app.providers.mock import MockProvider
from app.providers.fixture_loader import load_mock_fixtures


def get_provider(mode: str) -> ExtractionProvider:
    # Your implementation here
    if mode=='mock':
        return MockProvider(load_mock_fixtures())
    else:
        raise ValueError()
