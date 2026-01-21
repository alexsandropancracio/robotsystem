# tests/services/test_password_reset_service.py
from datetime import datetime, timezone, timedelta
import pytest

from backend.api.services.password_reset_service import PasswordResetService
from backend.api.models.password_reset_token import PasswordResetToken
from backend.tests.factories.user_factory import create_user
from backend.api.core.auth import verify_password
from backend.api.core.security.token import hash_token


def test_request_reset_creates_password_reset_token(db_session):
    # Arrange
    user = create_user(
        db=db_session,
        email="reset@test.com",
        is_active=True,
        is_email_verified=True,
    )

    # Act
    PasswordResetService.request_reset(
        db=db_session,
        email=user.email,
    )

    # Assert
    token = (
        db_session.query(PasswordResetToken)
        .filter(PasswordResetToken.user_id == user.id)
        .first()
    )

    assert token is not None
    assert token.used_at is None
    assert token.expires_at is not None
    assert token.expires_at > datetime.utcnow()


def test_request_reset_invalidates_old_tokens(db_session):
    # Arrange
    user = create_user(
        db=db_session,
        email="oldtoken@test.com",
    )

    PasswordResetService.request_reset(db_session, user.email)

    old_token = (
        db_session.query(PasswordResetToken)
        .filter(PasswordResetToken.user_id == user.id)
        .first()
    )

    assert old_token.used_at is None

    # Act
    PasswordResetService.request_reset(db_session, user.email)

    # Assert
    db_session.refresh(old_token)
    assert old_token.used_at is not None


def test_reset_password_success(db_session):
    # Arrange
    user = create_user(
        db=db_session,
        email="confirm@test.com",
        is_active=True,
        is_email_verified=True,
    )

    PasswordResetService.request_reset(db_session, user.email)

    reset_token = (
        db_session.query(PasswordResetToken)
        .filter(PasswordResetToken.user_id == user.id)
        .first()
    )

    raw_token = "valid-reset-token"
    reset_token.hashed_token = hash_token(raw_token)
    db_session.commit()

    new_password = "NovaSenha@123"

    # Act
    PasswordResetService.reset_password(
        db=db_session,
        token=raw_token,
        new_password=new_password,
        confirm_password=new_password,
    )

    # Assert
    db_session.refresh(user)
    db_session.refresh(reset_token)

    assert verify_password(new_password, user.hashed_password)
    assert reset_token.used_at is not None


def test_reset_password_invalid_token_raises_error(db_session):
    # Arrange
    user = create_user(db=db_session)

    PasswordResetService.request_reset(db_session, user.email)

    # Act / Assert
    with pytest.raises(ValueError):
        PasswordResetService.reset_password(
            db=db_session,
            token="token-invalido",
            new_password="Senha@123",
            confirm_password="Senha@123",
        )


def test_reset_password_expired_token_fails(db_session):
    # Arrange
    user = create_user(db=db_session)

    PasswordResetService.request_reset(db_session, user.email)

    reset_token = (
        db_session.query(PasswordResetToken)
        .filter(PasswordResetToken.user_id == user.id)
        .first()
    )

    raw_token = "expired-reset-token"
    reset_token.hashed_token = hash_token(raw_token)
    reset_token.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    db_session.commit()

    # Act / Assert
    with pytest.raises(ValueError):
        PasswordResetService.reset_password(
            db=db_session,
            token=raw_token,
            new_password="Senha@123",
            confirm_password="Senha@123",
        )
