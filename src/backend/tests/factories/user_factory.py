from backend.api.models.user import User


def create_user(
    *,
    email="test@example.com",
    is_active=False,
    is_email_verified=False,
):
    user = User(
        email=email,
        hashed_password="fake-hash",
        is_active=is_active,
        is_email_verified=is_email_verified,
    )
    return user
