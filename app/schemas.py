from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, ConfigDict, model_validator


class ExtractRequest(BaseModel):
    text: str = Field(min_length=10, max_length=1000)


class LeadFields(BaseModel):
    travelers: Optional[int] = Field(default=None, gt=0)
    contact_details: Optional[str] = None
    dates: Optional[date] = None
    location: Optional[str] = None
    duration: Optional[int] = Field(default=None, gt=0)
    origin_country: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    source_text: Optional[str] = None # Sensitive field snippet
    needs_review: bool = True

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_price_has_source(self):
        if self.price is not None and not self.source_text:
            raise ValueError("Imagined price rejected: price requires source_text.")
        return self


class ExtractResponse(BaseModel):
    leads: list[LeadFields]
    errors: list[str] = Field(default_factory=list)
    mode: str = "mock"  # "mock" ya "live" tag karne ke liye

    model_config = ConfigDict(extra="forbid")