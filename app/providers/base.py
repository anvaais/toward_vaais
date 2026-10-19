from typing import Protocol

from app.schemas import ExtractionResponse


class ProviderError(Exception):
    """Base class for safe provider errors."""


class ProviderUnavailableError(ProviderError):
    """The selected model provider could not complete the request."""


class ProviderOutputError(ProviderError):
    """The provider returned output that failed response validation."""


class ExtractionProvider(Protocol):
    def extract(self, raw_text: str) -> ExtractionResponse:
        ...
