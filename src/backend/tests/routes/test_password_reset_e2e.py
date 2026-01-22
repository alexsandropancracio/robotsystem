# backend/tests/routes/test_password_reset_e2e.py

import pytest
from fastapi.testclient import TestClient
from backend.api.deps.database import get_db
from backend.api.models.user import User
from backend.api.services.password_reset_service import PasswordResetService
from backend.api.core.mail.mail_service import MailService
from backend.tests.mocks.mail_client_mock import MailClientMock
from backend.api.core.auth import verify_password # 🔑 função de verificação de hash

@pytest.mark.asyncio
def test_password_reset_e2e(client: TestClient, db_session, user_factory):
    """
    E2E - Fluxo completo de reset de senha com token de 6 dígitos
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
    # 1️⃣ Criar usuário ativo
    # -------------------------
    user = user_factory(
        email="reset-test@robotsystem.com",
        password="oldpassword",
        is_active=True,
        is_email_verified=True,
    )

    # -------------------------
    # 2️⃣ Criar serviço de reset e mock de email
    # -------------------------
    mail_client = MailClientMock()
    mail_service = MailService(client=mail_client)
    reset_service = PasswordResetService(db=db_session, mail_service=mail_service)

    # -------------------------
    # 3️⃣ Solicitar reset de senha
    # -------------------------
    reset_service.request_reset(user.email)

    # ✅ Captura token do mock
    last_email = mail_client.last_email
    assert last_email is not None, "Nenhum e-mail foi enviado"
    reset_token = last_email["token"]
    assert reset_token is not None, "Token de reset não foi enviado"

    # -------------------------
    # 4️⃣ Resetar a senha usando o token
    # -------------------------
    new_password = "newpassword123"
    reset_service.reset_password(
        token=reset_token,
        new_password=new_password,
        confirm_password=new_password,
    )

    # -------------------------
    # 5️⃣ Validar se a senha foi atualizada
    # -------------------------
    updated_user: User = db_session.query(User).filter(User.id == user.id).first()
    assert updated_user is not None, "Usuário não encontrado no banco"

    # ✅ Verificação de hash da nova senha
    assert verify_password(new_password, updated_user.hashed_password), "Senha não foi atualizada corretamente"
