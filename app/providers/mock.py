from app.schemas import ExtractionResponse
class MockProvider:

    def __init__(
        self,
        fixtures: dict[str, ExtractionResponse],
        unknown_response: ExtractionResponse
    ) -> None:
        self.fixtures = fixtures
        self.unknown_response = unknown_response

    def extract(self, raw_text: str) -> ExtractionResponse:
        return self.fixtures.get(raw_text, self.unknown_response)
