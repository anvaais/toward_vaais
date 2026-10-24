import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
# from app.main import app, ExtractRequest, LeadFields
# from app.main import ExtractRequest, LeadFields,app
from app.main import app
from app.schemas import (
    ExtractRequest,
    LeadFields,
    ExtractionResponse
)

client = TestClient(app)

class FieldTypeKeys(BaseModel):
    explicit: list[str]
    derived: list[str]

class FixtureCase(BaseModel):
    id: str
    category: str
    input: ExtractRequest
    expected: LeadFields
    field_types: FieldTypeKeys

def load_fixtures():
    fixtures_path = Path(__file__).resolve().parent.parent / "data" / "fixtures.jsonl"
    with open(fixtures_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert len(lines) == 10, f"Expected 10 fixtures, found {len(lines)}"
    return [(json.loads(line)["id"], line) for line in lines]

@pytest.mark.parametrize("case_id, raw_line", load_fixtures())
def test_single_fixture_round_trip(case_id, raw_line):
    case = FixtureCase.model_validate_json(raw_line)
    revalidated = FixtureCase.model_validate(case.model_dump())
    assert revalidated.id == case_id

@pytest.mark.parametrize("case_id, raw_line", load_fixtures())
def test_extractor_returns_fixture_label(case_id, raw_line, monkeypatch):
    monkeypatch.setenv("PROVIDER_MODE", "mock")
    case = FixtureCase.model_validate_json(raw_line)

    response = client.post(
        "/extract",
        json=case.input.model_dump()
    )

    assert response.status_code == 200

    result = ExtractionResponse.model_validate(
        response.json()
    )

    assert len(result.leads) == 1
    assert result.errors == []
    assert result.leads[0] == case.expected