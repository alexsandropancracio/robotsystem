from app.service import AuthService
from app.user import UserRepository
from backend.api.database.session import SessionLocal

def get_auth_service():
    db = SessionLocal()  # ⚠️ placeholder para futuro
    repo = UserRepository(db)
    auth = AuthService(repo)
    return auth