from fastapi.testclient import TestClient
from app.main import app
from app.security import verify_api_key  # dependency override

# Bypass API key verification in tests
app.dependency_overrides[verify_api_key] = lambda: None

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_detect_pii_person():
    payload = {
        "text": "John Doe lives in New York.",
        "entities": ["PERSON"],
        "min_score": 0.1,
    }
    # Endpoint path: /v1/detect
    response = client.post("/v1/detect", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "entities" in data
    assert any(ent["type"] == "PERSON" for ent in data["entities"])


def test_redact_pii_person():
    payload = {
        "text": "John Doe lives in New York.",
        "policy": {
            "mask_mode": "template",
            "template": "{{ENTITY_TYPE}}",
            "entities_to_mask": ["PERSON"],
        },
    }
    # Endpoint path: /v1/redact
    response = client.post("/v1/redact", json=payload)
    assert response.status_code == 200
    result = response.json()["masked_text"]
    print(result)
    #  Code: Replaces the word “ENTITY_TYPE” within “{{ENTITY_TYPE}}” with “PERSON”
    # Result: “{{PERSON}}”
    assert "{{PERSON}}" in result
