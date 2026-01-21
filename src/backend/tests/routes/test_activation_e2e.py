# tests/routes/test_activation_e2e.py

import re
from fastapi.testclient import TestClient

from backend.api.deps.database import get_db
from backend.api.services.activation_token_service import ActivationTokenService
from backend.api.core.mail.mail_service import MailService
from backend.tests.mocks.mail_client_mock import MailClientMock


def test_activation_flow_e2e(
    client: TestClient,
    db_session,
    user_factory,
):
    """
    Teste E2E do fluxo completo de ativação de conta
    usando SQLite (isolado, sem tocar no Postgres)
    """

    # -------------------------------------------------
    # 🔁 Override REAL do get_db usado pelo FastAPI
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
            email="e2e@robotsystem.com",
            password="12345678",
            is_active=False,
            is_email_verified=False,
        )

        # -------------------------
        # 2️⃣ Gerar token de ativação
        # -------------------------
        mail_client = MailClientMock()
        mail_service = MailService(client=mail_client)

        ActivationTokenService(
            db=db_session,
            mail_service=mail_service,
        ).create_activation_token(user=user)

        assert mail_client.count == 1

        email_sent = mail_client.last_email
        assert email_sent is not None

        # Extrai token numérico de 6 dígitos do e-mail
        match = re.search(r"\b\d{6}\b", email_sent["text"])
        assert match is not None, "Token de ativação não encontrado no e-mail"

        token = match.group()

        # -------------------------
        # 3️⃣ Ativar conta via endpoint
        # -------------------------
        response = client.post(
            "/auth/activate",
            json={
                "email": user.email,
                "token": token,
            },
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Conta ativada com sucesso"

        # -------------------------
        # 4️⃣ Validar estado no banco
        # -------------------------
        db_session.refresh(user)

        assert user.is_active is True
        assert user.is_email_verified is True

    finally:
        # 🧹 Limpa overrides (MUITO importante)
        client.app.dependency_overrides.clear()

