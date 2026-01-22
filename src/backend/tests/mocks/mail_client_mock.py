import re
from typing import List, Dict


class MailClientMock:
    def __init__(self):
        self.sent_emails: List[Dict[str, str | None]] = []

    def send(
        self,
        *,
        to: str,
        subject: str,
        html_body: str,
        text_body: str,
        token: str | None = None,  # 👈 agora aceita token diretamente
    ) -> None:
        """
        Mock do cliente de e-mail.
        Captura o conteúdo enviado e extrai automaticamente tokens numéricos de 6 dígitos (ativação / reset),
        ou usa o token passado explicitamente.
        """
        if not token:
            match = re.search(r"token[:=]\s*([^\s]+)", text_body, re.IGNORECASE)
            token = match.group(1) if match else None

        self.sent_emails.append(
            {
                "to": to,
                "subject": subject,
                "html": html_body,
                "text": text_body,
                "token": token,  # 👈 token extraído ou passado diretamente
            }
        )

    def clear(self) -> None:
        self.sent_emails.clear()

    @property
    def last_email(self) -> dict | None:
        if not self.sent_emails:
            return None
        return self.sent_emails[-1]

    @property
    def count(self) -> int:
        return len(self.sent_emails)
