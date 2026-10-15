from fastapi import FastAPI
from fastapi.testclient import TestClient

# 1. Initialize the app first
app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": 200, "msg": "healthy"}


# 2. Pass the app instance into TestClient
client = TestClient(app)


# 3. Standard pytest function prefixed with 'test_'
def test_health():
    # Use the specific HTTP verb (.get) and match the exact route ("/health")
    response = client.get("/health")
    
    # Check .status_code and call .json()
    assert response.status_code == 200
    assert response.json() == {"status": 200, "msg": "healthy"}