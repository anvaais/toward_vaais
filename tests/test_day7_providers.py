import os

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.providers.base import ProviderUnavailableError, ProviderOutputError
from app.providers.fixture_loader import load_mock_fixtures
from app.providers.mock import MockProvider
from app.providers.factory import get_provider
from app.providers.gemini import GeminiProvider
from app.schemas import ExtractionResponse


client = TestClient(app)


def test_all_existing_fixtures_match():
    fixtures = load_mock_fixtures()
    assert len(fixtures) == 10
    provider = MockProvider(fixtures)
    for text, expected in fixtures.items():
        assert provider.extract(text) == expected
        assert isinstance(provider.extract(text), ExtractionResponse)


def test_mock_unknown_stays_unknown():
    provider = MockProvider(load_mock_fixtures())
    answer = provider.extract("A new client wants to discuss a holiday")
    assert answer.leads[0].travelers is None
    assert answer.leads[0].location is None
    assert answer.leads[0].needs_review is True


def test_mock_returns_independent_copies():
    provider = MockProvider(load_mock_fixtures())
    text = next(iter(provider.fixtures))
    first = provider.extract(text)
    first.leads[0].location = "Changed"
    assert provider.extract(text).leads[0].location == "Hunza"


def test_factory_selects_mock(monkeypatch):
    monkeypatch.setenv("PROVIDER_MODE", "mock")
    assert isinstance(get_provider(), MockProvider)


def test_factory_rejects_unknown_mode(monkeypatch):
    monkeypatch.setenv("PROVIDER_MODE", "invalid")
    with pytest.raises(ValueError, match="Unsupported PROVIDER_MODE"):
        get_provider()


def test_endpoint_returns_structured_mock(monkeypatch):
    monkeypatch.setenv("PROVIDER_MODE", "mock")
    text = next(iter(load_mock_fixtures()))
    response = client.post("/extract", json={"text": text})
    assert response.status_code == 200
    actual = ExtractionResponse.model_validate(response.json())
    assert actual.leads[0].travelers == 4
    assert actual.leads[0].location == "Hunza"


def test_endpoint_rejects_bad_request(monkeypatch):
    monkeypatch.setenv("PROVIDER_MODE", "mock")
    assert client.post("/extract", json={"text": "short"}).status_code == 422


def test_factory_gemini_missing_key(monkeypatch):
    monkeypatch.setenv("PROVIDER_MODE", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "")
    assert client.post(
        "/extract", json={"text": "We would like to visit Hunza next week"}
    ).status_code == 503


class FakeModels:
    def generate_content(self, **kwargs):
        raise RuntimeError("secret-fake-key-NEVER-EXPOSE")


class FakeClient:
    models = FakeModels()


def test_gemini_failure_is_safe():
    provider = GeminiProvider("dummy-key", "gemini-3.8-flash", client=FakeClient())
    with pytest.raises(ProviderUnavailableError) as exc:
        provider.extract("A synthetic customer message")
    assert "secret-fake-key" not in str(exc.value)

class BadResultModels:
    def generate_content(self, **kwargs):
        class BadResponse:
            parsed = None
            text = '{"leads": [{"travelers": -5}], "errors": []}'
        return BadResponse()


class BadResultClient:
    models = BadResultModels()


def test_gemini_invalid_output_rejected():
    provider = GeminiProvider("dummy-key", "gemini-3.8-flash", client=BadResultClient())
    with pytest.raises(ProviderOutputError):
        provider.extract("An example travel inquiry")


def test_no_hidden_fallback_on_provider_failure(monkeypatch):
    import app.main as main_module

    class FailingProvider:
        def extract(self, raw_text):
            raise ProviderUnavailableError("internal secret")

    monkeypatch.setattr(main_module, "get_provider", lambda: FailingProvider())
    response = client.post(
        "/extract", json={"text": "A customer inquiry to be processed"}
    )
    assert response.status_code == 502
    assert "secret" not in response.text
    assert "leads" not in response.text
