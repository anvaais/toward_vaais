import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, ValidationError

# ---------- Models ----------
class Offering(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    id: str
    destination: str
    service_type: str
    duration_days: int
    status: str
    indicative_note: str


class LookupOfferingInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    offering_id: str = Field(pattern=r"^[A-Za-z0-9_-]{1,64}$")


class LookupResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["found", "not_found"]
    offering: Offering | None = None


class ToolError(Exception):
    pass


# ---------- Fixed catalog path (model cannot change it) ----------
CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "catalog.json"


@lru_cache(maxsize=1)
def _load_catalog() -> dict[str, Offering]:
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return {o.id: o for o in (Offering(**item) for item in raw)}


# ---------- Tool ----------
def lookup_offering(offering_id: str) -> LookupResult:
    args = LookupOfferingInput(offering_id=offering_id)
    offering = _load_catalog().get(args.offering_id)
    if offering is None:
        return LookupResult(status="not_found")
    return LookupResult(status="found", offering=offering)


# ---------- Allowlist + schema ----------
ALLOWED_TOOLS = frozenset({"lookup_offering"})

TOOL_SCHEMAS = {
    "lookup_offering": {
        "description": "Look up one offering by its exact ID in the local catalog. Read-only.",
        "input_schema": LookupOfferingInput.model_json_schema(),
        "output_schema": LookupResult.model_json_schema(),
    }
}

_INPUT_MODELS = {"lookup_offering": LookupOfferingInput}


# ---------- Safe dispatcher ----------
def run_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name not in ALLOWED_TOOLS:
        raise ToolError(f"Tool not allowed: {name!r}")
    if not isinstance(arguments, dict):
        raise ToolError("Arguments must be an object.")
    try:
        validated = _INPUT_MODELS[name](**arguments)
    except ValidationError as exc:
        raise ToolError(f"Invalid arguments for {name!r}: {exc.error_count()} error(s)") from exc

    if name == "lookup_offering":
        return lookup_offering(**validated.model_dump()).model_dump()
    raise ToolError(f"Tool not implemented: {name!r}")



app = FastAPI(title="Agent Tools")


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    arguments: dict[str, Any] = {}


@app.get("/tools")
def list_tools():
    return TOOL_SCHEMAS


@app.post(
    "/tool",
    response_model=LookupResult,
    responses={
        400: {
            "description": "Unknown tool or invalid tool arguments"
        }
    },
)
def call_tool(call: ToolCall) -> LookupResult:
    try:
        return LookupResult.model_validate(run_tool(call.name, call.arguments))
    except ToolError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e