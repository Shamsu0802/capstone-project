from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert "running successfully" in response.json()["message"]


def test_empty_triage_request():

    response = client.post(
        "/triage",
        json={
            "patient_text": ""
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "failed"
    assert "error" in data


def test_short_triage_request():

    response = client.post(
        "/triage",
        json={
            "patient_text": "fever"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "failed"


def test_valid_triage_request():

    response = client.post(
        "/triage",
        json={
            "patient_text":
            "I have chest pain and shortness of breath since yesterday."
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "urgency" in data
    assert "recommendation" in data