import os
import pytest
import sys
# Agregar ruta a site-packages de venv para dependencias
venv_site = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'envqr', 'lib', 'python3.11', 'site-packages')
if os.path.isdir(venv_site):
    sys.path.insert(0, venv_site)
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
