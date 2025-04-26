import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthcheck():
    r = client.get("/v1/health")
    assert r.status_code == 200
    assert "status" in r.json()

@pytest.mark.parametrize("payload, status", [
    ({"email": "a@a.com", "password": "Pass1234"}, 201),
    ({}, 422),
])
def test_register(payload, status):
    r = client.post("/v1/auth/register", json=payload)
    assert r.status_code == status
