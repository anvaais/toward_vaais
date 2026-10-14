from fastapi import FastAPI,status
from pydantic import BaseModel,Field
from typing import List,Optional

app=FastAPI()

class ExtractRequest(BaseModel):
    text: str = Field(min_length=10, max_length=1000)


class LeadFields(BaseModel):
    travelers: Optional[int] = Field(default=None, gt=0)
    dates: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[int] = Field(default=None, gt=0)
    origin_country: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    needs_review: Optional[bool] = False

class ExtractionResponse(BaseModel):
    leads: list[LeadFields]
    errors: list[str] = Field(default_factory=list)

@app.post("/extract",status_code=status.HTTP_200_OK,response_model=ExtractionResponse)
async def extractor(request:ExtractRequest)->ExtractionResponse:
    stub_lead = LeadFields(travelers=4,dates="12 oct",location="skardu",duration=3,origin_country="canda",price=490,)
    re={
        "leads":[stub_lead],
        "errors":[]
    }
    return re