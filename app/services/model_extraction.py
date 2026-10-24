import json
from pydantic import ValidationError
from app.schemas import LeadFields, ExtractResponse
from app.prompts import EXTRACTION_INSTRUCTIONS


def validate_model_output(raw_output: str, inquiry_text: str = "") -> ExtractResponse:
    """Validate the AI model's JSON output before using it."""
    try:
        # Pydantic khud JSON parse karega aur LeadFields + extra="forbid" check karega
        response = ExtractResponse.model_validate_json(raw_output)

        # Safety check: Kya source_text waqai original inquiry_text mein maujood hai?
        if inquiry_text:
            for lead in response.leads:
                if lead.price is not None:
                    if not lead.source_text or lead.source_text.lower() not in inquiry_text.lower():
                        raise ValueError("Price source_text not found in original inquiry!")

        return response

    except (ValidationError, ValueError) as exc:
        raise ValueError(f"Invalid model output: {exc}") from exc


def extract_from_inquiry(inquiry_text: str, mode: str = "mock") -> ExtractResponse:
    """Request structured extraction (mock or live) and pass through validation boundary."""
    _prompt = f"{EXTRACTION_INSTRUCTIONS}\n\nInquiry:\n{inquiry_text}"

    if mode == "mock":
        text_lower = inquiry_text.lower()
        # Vague date ya contradictory message check
        if "maybe" in text_lower or "next month" in text_lower or "actually" in text_lower:
            raw_json = json.dumps({
                "leads": [{"dates": None, "travelers": None, "needs_review": True}],
                "errors": [],
                "mode": "mock"
            })
        else:
            raw_json = json.dumps({
                "leads": [{
                    "travelers": 2,
                    "location": "Skardu",
                    "dates": "2026-11-10",
                    "needs_review": False
                }],
                "errors": [],
                "mode": "mock"
            })
        return validate_model_output(raw_json, inquiry_text=inquiry_text)

    raise NotImplementedError("Live mode not configured yet.")