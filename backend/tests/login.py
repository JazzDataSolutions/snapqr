#!/usr/bin/env python3
"""
Hace login y muestra tokens.
Uso: python scripts/login.py
"""
import os, requests
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("API_URL", "http://localhost:8000/v1")
email = "juan.perez@example.com"
password = "Password123"

resp = requests.post(f"{API}/auth/login", json={
    "email": email,
    "password": password
})
resp.raise_for_status()
print("Login response:", resp.json())

