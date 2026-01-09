# backend/api/routes/health.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.api.deps.database import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health_check(db: Session = Depends(get_db)):
    """
    Verifica se a API e o banco de dados estão funcionando.
    """
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "database": db_status,
    }
