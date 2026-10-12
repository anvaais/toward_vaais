from fastapi import FastAPI

app=FastAPI(
    title="VA-AIS",
    description="VA-AIS is a virtual AI agent system that can be used to create and manage AI agents for various tasks.",
    version="0.1.0",
)

@app.get("/health",status_code=200)
async def root():
    return {
        "status": "healthy",
        "service": "vaais-core",
        "environment": "development",
    }