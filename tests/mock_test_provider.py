
from datetime import date
from app.schemas import LeadFields, ExtractionResponse
from app.providers.mock import MockProvider

complete_text = (
    "We are 4 travelers from Pakistan planning a "
    "5-day trip to Skardu starting November 15, 2026. "
    "Our budget is PKR 75,000."
)

complete_response = ExtractionResponse(
    leads=[
        LeadFields(
            travelers=4,
            dates=date(2026, 11, 15),
            location="Skardu",
            duration=5,
            origin_country="Pakistan",
            price=75000.0,
            needs_review=False
        )
    ],
    errors=[]
)
