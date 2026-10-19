
import json
from pathlib import Path

from app.schemas import (
    ExtractRequest,
    LeadFields,
    ExtractionResponse
)
from app.providers.mock import MockProvider


fixture_path = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "fixtures.jsonl"
)

records = [
    json.loads(line)
    for line in fixture_path.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

fixtures = {}

for record in records:
    inquiry = ExtractRequest.model_validate(
        record["input"]
    )

    expected = LeadFields.model_validate(
        record["expected"]
    )

    fixtures[inquiry.text] = ExtractionResponse(
        leads=[expected],
        errors=[]
    )

provider = MockProvider(fixtures)


def test_mock_matches_existing_labels():
    assert len(records) == 10

    for record in records:
        text = record["input"]["text"]
        actual = provider.extract(text)

        expected = LeadFields.model_validate(
            record["expected"]
        )

        assert actual.leads[0] == expected


def test_mock_unknown_input():
    response = provider.extract(
        "A new customer wants to discuss a trip"
    )

    assert response.leads[0].travelers is None
    assert response.leads[0].location is None
    assert response.leads[0].needs_review is True


def test_mock_deterministic():
    text = records[0]["input"]["text"]

    first = provider.extract(text)
    second = provider.extract(text)

    assert first == second


def test_mock_returns_independent_copies():
    text = records[0]["input"]["text"]

    first = provider.extract(text)
    first.leads[0].location = "Changed"

    second = provider.extract(text)

    assert second.leads[0].location == "Hunza"
