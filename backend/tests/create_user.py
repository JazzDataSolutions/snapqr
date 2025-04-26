#!/usr/bin/env python3
"""
Crea un usuario de prueba (register).
Uso: python scripts/create_user.py
"""
import os, requests
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("API_URL", "http://localhost:8000/v1")
email = "juan.perez@example.com"
password = "Password123"

resp = requests.post(f"{API}/auth/register", json={
    "email": email,
    "password": password
})
resp.raise_for_status()
print("Usuario creado:", resp.json())

