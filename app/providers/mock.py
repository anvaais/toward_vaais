
from app.schemas import ExtractionResponse, LeadFields


class MockProvider:

    def __init__(
        self,
        fixtures: dict[str, ExtractionResponse]
    ):
        self.fixtures = fixtures

    def extract(self, raw_text: str) -> ExtractionResponse:
        response = self.fixtures.get(raw_text)

        if response is not None:
            return response.model_copy(deep=True)

        return ExtractionResponse(
            leads=[LeadFields(needs_review=True)],
            errors=[]
        )
