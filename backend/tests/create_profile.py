#!/usr/bin/env python3
"""
Crea/actualiza perfil, sube foto de perfil.
Uso: python scripts/create_profile.py /ruta/a/foto.jpg
"""
import os, sys, requests
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("API_URL", "http://localhost:8000/v1")
token = os.getenv("ACCESS_TOKEN")  # o pasar por args

if len(sys.argv) < 2:
    print("Uso: create_profile.py <ruta_foto>")
    sys.exit(1)

foto_path = sys.argv[1]
headers = {"Authorization": f"Bearer {token}"}
data = {"nombre": "Juan Pérez"}
files = {"foto": open(foto_path, "rb")}

resp = requests.post(
    f"{API}/users/profile",
    headers=headers,
    data=data,
    files=files
)
resp.raise_for_status()
print("Perfil actualizado:", resp.json())

