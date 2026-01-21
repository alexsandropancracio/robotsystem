# backend/api/main.py
from fastapi import FastAPI

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from backend.api.core.config import get_settings
from backend.api.core.security.rate_limiter import limiter
from backend.api.routes import users, auth, health, me


settings = get_settings()

app = FastAPI(
    title=settings.API_NAME,
    version=settings.API_VERSION,
)

# -------------------------------------------------
# RATE LIMIT (GLOBAL)
# -------------------------------------------------
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

# -------------------------------------------------
# ROUTERS
# -------------------------------------------------
app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(me.router)
