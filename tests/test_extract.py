from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    # Arrange & Act
    response = client.get("/health")
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_extract_basic_valid_request():
    # Arrange
    payload = {"text": "We are 4 people looking to travel from Islamabad to Skardu for 5 days next week with a budget of 50000."}
    
    # Act
    response = client.post("/extract", json=payload)
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "leads" in data
    assert "errors" in data
    assert isinstance(data["leads"], list)

def test_extract_absent_traveler_count():
    # Arrange: Inquiry with no traveler count mentioned
    payload = {"text": "We want to visit Skardu in July for a trek."}
    
    # Act
    response = client.post("/extract", json=payload)
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert data["leads"][0]["travelers"] is None

def test_extract_invalid_field_type():
    # Arrange: Sending an integer instead of string for 'text'
    payload = {"text": 12345}
    
    # Act
    response = client.post("/extract", json=payload)
    data = response.json()
    
    # Assert
    assert response.status_code == 422
    assert "detail" in data

def test_extract_malformed_json():
    # Arrange: Sending raw broken JSON syntax using content=
    broken_json = '{"text": "missing closing quote'
    
    # Act
    response = client.post(
        "/extract",
        content=broken_json,
        headers={"Content-Type": "application/json"}
    )
    
    # Assert
    assert response.status_code == 422
    assert "detail" in response.json()
