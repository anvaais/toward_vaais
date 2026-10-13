import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from pydantic import BaseModel,Field
from typing import Optional
from datetime import date




## Day two task
class ExtractRequest(BaseModel):
    text:str=Field(min_length=10, max_length=1000)

class LeadFields(BaseModel):
    travelers: Optional[int] = Field(default=None, gt=0)
    dates: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[int] = Field(default=None, gt=0)
    origin_country: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    needs_review: Optional[bool] = None

class ExtractionResponse(BaseModel):
    leads: list[LeadFields]
    status: str
    

class ExtractionResponse(BaseModel):
    leads: list[LeadFields]
    errors: list[str] = Field(default_factory=list)



@pytest.mark.asyncio
async def test_health_check_returns_200():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "vaais-core"
    assert "environment" in data
