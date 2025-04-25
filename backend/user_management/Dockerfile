# Usamos una imagen base de Python
FROM python:3.9-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements y posteriormente instalar (para aprovechar la cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto donde correrá FastAPI
EXPOSE 8000

# Comando para ejecutar FastAPI con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
