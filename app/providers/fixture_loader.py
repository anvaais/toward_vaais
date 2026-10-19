import json
from pathlib import Path

from app.schemas import ExtractRequest, ExtractionResponse, LeadFields


FIXTURE_FILE = Path(__file__).resolve().parents[2] / "data" / "fixtures.jsonl"


def load_mock_fixtures(path: Path = FIXTURE_FILE) -> dict[str, ExtractionResponse]:
    """Validate existing Day 5 fixtures; never import models from tests/."""
    fixtures: dict[str, ExtractionResponse] = {}
    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            raw_text = ExtractRequest.model_validate(record["input"]).text
            label = LeadFields.model_validate(record["expected"])
            if raw_text in fixtures:
                raise ValueError(f"Duplicate fixture input at line {line_number}")
            fixtures[raw_text] = ExtractionResponse(leads=[label], errors=[])
    return fixtures
