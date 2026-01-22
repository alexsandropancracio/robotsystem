from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import re

from backend.api.services.activation_token_service import ActivationTokenService
from backend.api.core.mail.mail_service import MailService
from backend.tests.mocks.mail_client_mock import MailClientMock
from backend.api.deps.database import get_db
from backend.api.models.activation_token import ActivationToken


def test_activation_with_expired_token_e2e(
    client: TestClient,
    db_session,
    user_factory,
):
    """
    E2E - Tentativa de ativação com token expirado
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

    try:
        # -------------------------
        # 1️⃣ Criar usuário inativo
        # -------------------------
        user = user_factory(
            email="expired-token@robotsystem.com",
            password="12345678",
            is_active=False,
            is_email_verified=False,
        )

        # -------------------------
        # 2️⃣ Gerar token normalmente
        # -------------------------
        mail_client = MailClientMock()
        mail_service = MailService(client=mail_client)

        ActivationTokenService(
            db=db_session,
            mail_service=mail_service,
        ).create_activation_token(user=user)

        assert mail_client.count == 1

        email_sent = mail_client.last_email
        match = re.search(r"\b\d{6}\b", email_sent["text"])
        assert match is not None

        token = match.group()

        # -------------------------
        # 3️⃣ Forçar expiração do token no banco
        # -------------------------
        activation_token = (
            db_session.query(ActivationToken)
            .filter(ActivationToken.user_id == user.id)
            .first()
        )

        assert activation_token is not None

        activation_token.expires_at = datetime.utcnow() - timedelta(minutes=1)
        db_session.commit()

        # -------------------------
        # 4️⃣ Tentar ativar conta
        # -------------------------
        response = client.post(
            "/auth/activate",
            json={
                "email": user.email,
                "token": token,
            },
        )

        # -------------------------
        # 5️⃣ Validar resposta
        # -------------------------
        assert response.status_code == 400
        assert "expirado" in response.json()["detail"].lower()

        # -------------------------
        # 6️⃣ Validar estado no banco
        # -------------------------
        db_session.refresh(user)

        assert user.is_active is False
        assert user.is_email_verified is False

    finally:
        client.app.dependency_overrides.clear()
