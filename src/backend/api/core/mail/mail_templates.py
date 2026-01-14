# backend/api/core/mail/mail_templates.py
from typing import Tuple

# -------------------------------------------------
# Template de e-mail de ativação de conta
# -------------------------------------------------
def activation_email_template(
    *,
    user_email: str,
    activation_token: str,
    app_name: str = "RobotSystem",
    expires_in_minutes: int | None = None,
) -> Tuple[str, str, str]:
    """
    Gera o template de e-mail para ativação de conta.

    Retorna:
        subject (str)
        text_body (str)
        html_body (str)
    """
    expires_minutes = expires_in_minutes or 15

    subject = f"Ative sua conta no {app_name}"

    text_body = f"""
Olá,

Você criou uma conta no {app_name} usando o e-mail {user_email}.

Para ativar sua conta, utilize o código abaixo:

Código de ativação: {activation_token}

Se você não solicitou este cadastro, ignore este e-mail.

— Equipe {app_name}
""".strip()

    html_body = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{subject}</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 24px; border-radius: 8px;">
        <h2 style="color: #333333;">Ativação de conta</h2>

        <p>Olá,</p>

        <p>
            Você criou uma conta no <strong>{app_name}</strong> usando o e-mail
            <strong>{user_email}</strong>.
        </p>

        <p>Para ativar sua conta, utilize o código abaixo:</p>

        <div style="
            font-size: 24px;
            font-weight: bold;
            letter-spacing: 4px;
            text-align: center;
            padding: 16px;
            background-color: #f0f0f0;
            border-radius: 6px;
            margin: 20px 0;
        ">
            {activation_token}
        </div>

        <p style="color: #777777; font-size: 14px;">
            Se você não solicitou este cadastro, apenas ignore este e-mail.
        </p>

        <hr style="margin: 24px 0;">

        <p style="font-size: 12px; color: #999999;">
            © {app_name}
        </p>
    </div>
</body>
</html>
""".strip()

    return subject, text_body, html_body
