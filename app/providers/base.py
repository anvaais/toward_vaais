from typing import Protocol
from app.schemas import ExtractionResponse



class ExtractionProvider(Protocol):
    def extract(self, raw_text: str) -> ExtractionResponse:
        ...