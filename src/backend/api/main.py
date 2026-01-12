#backend/api/main.py
from fastapi import FastAPI
from backend.api.core.config import get_settings
from backend.api.routes import users, auth, health, me


settings = get_settings()

app = FastAPI(
    title=settings.API_NAME,
    version=settings.API_VERSION,
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(me.router)