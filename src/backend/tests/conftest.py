import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.api.database.base import Base
from backend.api.models.user import User


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def user_factory(db_session):
    def _factory(**kwargs):
        user = User(
            email=kwargs.get("email", "test@example.com"),
            hashed_password=kwargs.get("hashed_password", "fake-hash"),
            is_active=kwargs.get("is_active", False),
            is_email_verified=kwargs.get("is_email_verified", False),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _factory