from backend.api.deps.database import get_db


def test_activation_user_already_active_e2e(
    client,
    db_session,
    user_factory,
):
    """
    E2E - Tentativa de ativação de usuário já ativo
    """

    # -------------------------------------------------
    # Override do get_db para usar SQLite do teste
    # -------------------------------------------------
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    client.app.dependency_overrides[get_db] = override_get_db

    try:
        # -------------------------
        # Criar usuário JÁ ativo
        # -------------------------
        user = user_factory(
            email="active@robotsystem.com",
            password="12345678",
            is_active=True,
            is_email_verified=True,
        )

        # -------------------------
        # Tentar ativar novamente
        # -------------------------
        response = client.post(
            "/auth/activate",
            json={
                "email": user.email,
                "token": "123456",  # qualquer token
            },
        )

        # -------------------------
        # Assert
        # -------------------------
        assert response.status_code == 400
        assert response.json()["detail"] == "Conta já está ativada"

    finally:
        client.app.dependency_overrides.clear()
