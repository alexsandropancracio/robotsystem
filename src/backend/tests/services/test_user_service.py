import pytest

from backend.api.schemas.user import UserCreate
from backend.api.services.user_service import (
    create_user_service,
    list_users_service,
    get_user_service,
)
from backend.api.core.exceptions import UserAlreadyExistsError


# -------------------------------------------------
# CREATE USER
# -------------------------------------------------

def test_create_user_success(db_session):
    user_in = UserCreate(
        email="test@example.com",
        password="Test@1234",
        full_name="Test User",
    )

    user = create_user_service(db_session, user_in)

    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is False


def test_create_user_duplicate_email_raises_error(db_session):
    user_in = UserCreate(
        email="duplicate@example.com",
        password="Test@1234",
    )

    create_user_service(db_session, user_in)

    with pytest.raises(UserAlreadyExistsError):
        create_user_service(db_session, user_in)


# -------------------------------------------------
# LIST USERS
# -------------------------------------------------

def test_list_users_returns_list(db_session):
    users = list_users_service(db_session)

    assert isinstance(users, list)


def test_list_users_contains_created_user(db_session):
    user_in = UserCreate(
        email="list@example.com",
        password="Test@1234",
    )

    create_user_service(db_session, user_in)

    users = list_users_service(db_session)

    emails = [user.email for user in users]
    assert "list@example.com" in emails


# -------------------------------------------------
# GET USER
# -------------------------------------------------

def test_get_user_by_id_returns_user(db_session):
    user_in = UserCreate(
        email="get@example.com",
        password="Test@1234",
    )

    created_user = create_user_service(db_session, user_in)

    user = get_user_service(db_session, created_user.id)

    assert user is not None
    assert user.email == "get@example.com"


def test_get_user_by_invalid_id_returns_none(db_session):
    user = get_user_service(db_session, user_id=9999)

    assert user is None
