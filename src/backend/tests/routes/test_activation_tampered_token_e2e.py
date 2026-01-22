import pytest
from fastapi.testclient import TestClient

from backend.api.services.activation_token_service import ActivationTokenService
from backend.api.deps.database import get_db
from backend.api.models.user import User
from backend.tests.mocks.mail_client_mock import MailClientMock
from backend.api.core.mail.mail_service import MailService


@pytest.mark.asyncio
def test_activation_with_tampered_token_e2e(client: TestClient, db_session, user_factory):
    """
    E2E - Tentativa de ativação com token adulterado
    """

    # -------------------------------------------------
    # 🔁 Override do get_db para usar SQLite do teste
    # -------------------------------------------------
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    client.app.dependency_overrides[get_db] = override_get_db

    # -------------------------
    # 1️⃣ Criar usuário inativo
    # -------------------------
    user = user_factory(
        email="tampered-token@robotsystem.com",
        password="12345678",
        is_active=False,
        is_email_verified=False,
    )

    # -------------------------
    # 2️⃣ Gerar token "válido"
    # -------------------------
    mail_client = MailClientMock()
    mail_service = MailService(client=mail_client)

    token_service = ActivationTokenService(db=db_session, mail_service=mail_service)
    valid_token = token_service.create_activation_token(user=user)

    # -------------------------
    # 3️⃣ Alterar o token para simular adulteração
    # -------------------------
    tampered_token = valid_token + "123"

    # -------------------------
    # 4️⃣ Tentar ativar com token adulterado
    # -------------------------
    response = client.post(
        "/auth/activate",
        json={
            "email": user.email,
            "token": tampered_token,
        },
    )

    # -------------------------
    # 5️⃣ Assert
    # -------------------------
    assert response.status_code == 400
    assert response.json()["detail"] == "Token inválido ou expirado"

