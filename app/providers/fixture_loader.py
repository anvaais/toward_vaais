
import json
from pathlib import Path

from app.schemas import (
    ExtractRequest,
    LeadFields,
    ExtractionResponse
)


def load_mock_fixtures() -> dict[str, ExtractionResponse]:
    path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "fixtures.jsonl"
    )

    fixtures = {}

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            record = json.loads(line)

            request = ExtractRequest.model_validate(
                record["input"]
            )

            expected = LeadFields.model_validate(
                record["expected"]
            )

            if request.text in fixtures:
                raise ValueError("Duplicate fixture input")

            fixtures[request.text] = ExtractionResponse(
                leads=[expected],
                errors=[]
            )

    return fixtures
