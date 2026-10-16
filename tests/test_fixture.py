import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from app.main import app, ExtractRequest, LeadFields

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
def test_extractor_mismatches(case_id, raw_line):
    case = FixtureCase.model_validate_json(raw_line)
    response = client.post("/extract", json=case.input.model_dump())
    assert response.status_code == 200

    expected_dict = case.expected.model_dump()
    actual_dict = response.json()
    

    mismatches = []
    for key, expected_val in expected_dict.items():
        actual_val = actual_dict.get(key)
        if expected_val != actual_val:
            mismatches.append((case_id, key, expected_val, actual_val))

    for case_id_val, field, exp, act in mismatches:
        print(f"MISMATCH [{case_id_val}] {field}: expected={exp!r}, actual={act!r}")