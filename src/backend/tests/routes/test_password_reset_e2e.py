import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.api.main import app
from backend.api.deps.database import get_db
from backend.api.models.user import Base, User
from backend.api.services.password_reset_service import PasswordResetService
from backend.tests.mocks.mail_client_mock import MailClientMock
from backend.api.core.mail.mail_service import MailService

# ------------------------------
# Configuração do DB de teste
# ------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Sobrescrevendo a dependência do DB para usar o SQLite de teste
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ------------------------------
# Mock de e-mail
# ------------------------------
mail_client_mock = MailClientMock()
mail_service = MailService(mail_client=mail_client_mock)

# ------------------------------
# Cliente de teste FastAPI
# ------------------------------
client = TestClient(app)

# ------------------------------
# Teste E2E do Password Reset
# ------------------------------
def test_password_reset_flow():
    # 1️⃣ Criar usuário de teste
    db = next(override_get_db())
    test_user = User(
        email="user@example.com",
        hashed_password="oldhashedpassword",
        is_active=True,
        is_email_verified=True
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    # 2️⃣ Solicitar redefinição de senha
    response_request = client.post(
        "/auth/password-reset/request",
        json={"email": test_user.email}
    )
    assert response_request.status_code == 200
    assert "Se o e-mail existir" in response_request.json()["message"]

    # 3️⃣ Capturar token do mock
    reset_token = mail_client_mock.last_reset_token
    assert reset_token is not None, "O token de reset não foi gerado"

    # 4️⃣ Confirmar redefinição de senha
    new_password = "newsecurepassword123"
    response_confirm = client.post(
        "/auth/password-reset/confirm",
        json={
            "token": reset_token,
            "new_password": new_password,
            "confirm_password": new_password
        }
    )
    assert response_confirm.status_code == 200
    assert "Senha redefinida com sucesso" in response_confirm.json()["message"]

    # 5️⃣ Verificar que a senha realmente mudou no DB
    db.refresh(test_user)
    assert test_user.hashed_password != "oldhashedpassword"
