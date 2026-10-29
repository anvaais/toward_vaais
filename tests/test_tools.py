import pytest
from fastapi.testclient import TestClient

from app.agent.tools import (
    TOOL_SCHEMAS,
    app,
    run_tool,
    ToolError,
    lookup_offering,
)

client = TestClient(app)


def test_known_offering():
    result = lookup_offering("1")

    assert result.status == "found"
    assert result.offering is not None
    assert result.offering.id == "1"
    assert result.offering.destination == "Skardu"


def test_unknown_offering():
    result = lookup_offering("UNKNOWN-ID")

    assert result.status == "not_found"
    assert result.offering is None


@pytest.mark.parametrize(
    "arguments",
    [
        {},
        {"offering_id": 123},
        {"offering_id": "1", "extra_field": "unexpected"},
        {"offering_id": "bad id"},
    ],
)
def test_invalid_arguments(arguments):
    with pytest.raises(ToolError):
        run_tool("lookup_offering", arguments)


def test_unapproved_tool():
    with pytest.raises(ToolError):
        run_tool("delete_catalog", {})


def test_tool_endpoint_returns_record():
    response = client.post(
        "/tool",
        json={
            "name": "lookup_offering",
            "arguments": {"offering_id": "1"},
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "found"


def test_tool_endpoint_rejects_extra_arguments():
    response = client.post(
        "/tool",
        json={
            "name": "lookup_offering",
            "arguments": {
                "offering_id": "1",
                "extra_field": "unexpected",
            },
        },
    )

    assert response.status_code == 400
    assert "Invalid arguments" in response.json()["detail"]



def test_non_object_arguments_are_rejected():
    with pytest.raises(
        ToolError,
        match="Arguments must be an object",
    ):
        run_tool("lookup_offering", None)


def test_input_schema_is_restricted():
    schema = TOOL_SCHEMAS["lookup_offering"]["input_schema"]

    assert schema["type"] == "object"
    assert schema["required"] == ["offering_id"]
    assert schema["additionalProperties"] is False

    argument_schema = schema["properties"]["offering_id"]

    assert argument_schema["type"] == "string"
    assert argument_schema["pattern"] == r"^[A-Za-z0-9_-]{1,64}$"


def test_output_schema_describes_lookup_result():
    schema = TOOL_SCHEMAS["lookup_offering"]["output_schema"]

    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False

    properties = schema["properties"]

    assert properties["status"]["enum"] == [
        "found",
        "not_found",
    ]
    assert "offering" in properties

    offering_schema = schema["$defs"]["Offering"]

    expected_fields = {
        "id",
        "destination",
        "service_type",
        "duration_days",
        "status",
        "indicative_note",
    }

    assert expected_fields.issubset(
        set(offering_schema["properties"])
    )