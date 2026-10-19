from fastapi import FastAPI, HTTPException, status
from starlette.concurrency import run_in_threadpool

from app.schemas import ExtractRequest, ExtractionResponse, LeadFields
from app.providers.base import ProviderOutputError, ProviderUnavailableError
from app.providers.factory import get_provider


app = FastAPI(
    title="VA-AIS",
    description="VA-AIS is a virtual AI agent system that can be used to create and manage AI agents for various tasks.",
    version="0.1.0",
)


@app.get("/health", status_code=200)
async def root():
    return {"status": "ok"}


@app.post("/extract", status_code=status.HTTP_200_OK, response_model=ExtractionResponse)
async def extractor(request: ExtractRequest) -> ExtractionResponse:
    try:
        provider = get_provider()
    except ValueError:
        raise HTTPException(
            status_code=503,
            detail="Provider configuration error",
        ) from None

    try:
        # The SDK has a synchronous client; keep it off the async event loop.
        return await run_in_threadpool(provider.extract, request.text)
    except ProviderUnavailableError:
        raise HTTPException(
            status_code=502, detail="Selected AI provider is unavailable"
        ) from None
    except ProviderOutputError:
        raise HTTPException(
            status_code=502, detail="Provider returned invalid structured output"
        ) from None
