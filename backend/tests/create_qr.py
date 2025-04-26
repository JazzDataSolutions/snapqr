#!/usr/bin/env python3
"""
Genera un QR para un userId dado.
Uso: python scripts/generate_qr.py 1
"""
import os, sys, requests
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("API_URL", "http://localhost:8000/v1")
token = os.getenv("ACCESS_TOKEN")

if len(sys.argv) < 2:
    print("Uso: generate_qr.py <user_id>")
    sys.exit(1)

user_id = sys.argv[1]
headers = {"Authorization": f"Bearer {token}"}

resp = requests.post(f"{API}/qr/{user_id}", headers=headers)
resp.raise_for_status()
qr = resp.json()
print("QR generado:", qr)

