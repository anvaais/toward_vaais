from datetime import date
from typing import Optional

from fastapi import FastAPI,status
from pydantic import BaseModel, Field


app = FastAPI(
    title="VA-AIS",
    description="VA-AIS is a virtual AI agent system that can be used to create and manage AI agents for various tasks.",
    version="0.1.0",
)


class ExtractRequest(BaseModel):
    text: str = Field(min_length=10, max_length=1000)


class LeadFields(BaseModel):
    travelers: Optional[int] = Field(default=None, gt=0)
    dates: Optional[date] = None
    location: Optional[str] = None
    duration: Optional[int] = Field(default=None, gt=0)
    origin_country: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    needs_review: Optional[bool] = None


class ExtractionResponse(BaseModel):
    leads: list[LeadFields]
    errors: list[str] = Field(default_factory=list)

error={
  "detail": [
    {
      "type": "greater_than",
      "loc": [
        "body",
        "leads",
        0,
        "travelers"
      ],
      "msg": "Input should be greater than 0",
      "input": 0,
      "ctx": {
        "gt": 0
      }
    },
    {
      "type": "greater_than",
      "loc": [
        "body",
        "leads",
        0,
        "price"
      ],
      "msg": "Input should be greater than 0",
      "input": -25,
      "ctx": {
        "gt": 0
      }
    }
  ]
}

@app.get("/health", status_code=200)
async def root():
    return {
        "status": "ok",
    }
@app.post("/extract", status_code=status.HTTP_200_OK, response_model=ExtractionResponse)
async def extractor(request: ExtractRequest) -> ExtractionResponse:
    # A true safe stub returning explicit unknowns for unextracted fields
    stub_lead = LeadFields(
        travelers=None, 
        dates=None, 
        location="unknown" if "skardu" not in request.text.lower() else "skardu", 
        duration=None, 
        origin_country=None, 
        price=None,
        needs_review=True
    )
    return ExtractionResponse(leads=[stub_lead], errors=[])
