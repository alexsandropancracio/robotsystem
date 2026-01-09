from fastapi import APIRouter, Depends
from backend.api.deps.license import get_current_user_with_license
from backend.api.models.user import User

router = APIRouter(
    prefix="/protected",
    tags=["Protected"],
)

@router.get("/")
def protected_route(
    current_user: User = Depends(get_current_user_with_license),
):
    return {
        "message": "Acesso liberado",
        "user_id": current_user.id,
        "email": current_user.email,
    }
