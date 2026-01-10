from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.deps.database import get_db
from backend.api.schemas.auth import RefreshTokenRequest
from backend.api.schemas.user import UserLogin, Token
from backend.api.services.auth_service import login_service
from backend.api.services.refresh_token_service import RefreshTokenService
from backend.api.core.auth import create_access_token
from backend.api.core.exceptions import InvalidCredentialsError

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
@router.post("/login", response_model=Token)
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        return login_service(
            db,
            user_in.email,
            user_in.password,
        )

    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


# -------------------------------------------------
# LOGOUT
# -------------------------------------------------
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    refresh_service = RefreshTokenService(db)

    revoked = refresh_service.revoke_refresh_token(data.refresh_token)
    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token inválido ou já revogado",
        )


# -------------------------------------------------
# REFRESH TOKEN
# -------------------------------------------------
@router.post("/refresh", response_model=Token)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    refresh_service = RefreshTokenService(db)

    result = refresh_service.rotate_refresh_token(data.refresh_token)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
        )

    user, new_refresh_token = result

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
    )
