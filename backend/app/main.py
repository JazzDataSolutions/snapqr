from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .config import settings
from .db import init_db
from .routers import auth, users, qr, photos

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR + "/users", tags=["users"])
app.include_router(qr.router, prefix=settings.API_V1_STR + "/qr", tags=["qr"])
app.include_router(photos.router, prefix=settings.API_V1_STR + "/photos", tags=["photos"])

@app.on_event("startup")
def on_startup():
    init_db()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse({"detail": str(exc)}, status_code=500)

