from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_and_cipher_catalog():
    assert client.get("/api/health").json()["status"] == "ok"
    assert len(client.get("/api/ciphers").json()) == 8


def test_encrypt_validation_error():
    response = client.post("/api/encrypt", json={"algorithm": "caesar", "text": "HELLO", "key": "bad"})
    assert response.status_code == 422
    assert "integer" in response.json()["detail"]


def test_file_encrypt_endpoint():
    response = client.post("/api/files/encrypt", files={"file": ("sample.txt", "HELLO", "text/plain")}, data={"algorithm": "caesar", "key": "3"})
    assert response.status_code == 200
    assert response.json()["result"] == "KHOOR"
