#!/usr/bin/env python3
"""
Sube una foto de evento y muestra los usuarios detectados.
Uso: python scripts/upload_photo.py /ruta/a/foto_evento.jpg
"""
import os, sys, requests
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("API_URL", "http://localhost:8000/v1")
token = os.getenv("ACCESS_TOKEN")

if len(sys.argv) < 2:
    print("Uso: upload_photo.py <ruta_foto_evento>")
    sys.exit(1)

foto_path = sys.argv[1]
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open(foto_path, "rb")}

resp = requests.post(f"{API}/photos/upload", headers=headers, files=files)
resp.raise_for_status()
print("Upload response:", resp.json())

