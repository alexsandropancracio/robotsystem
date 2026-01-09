from app.service import AuthService
from app.user import UserRepository

def get_auth_service():
    repo = UserRepository()
    return AuthService(user_repo=repo)
