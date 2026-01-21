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
    ) -> None:
        """
        Mock do cliente de e-mail.
        Captura o conteúdo enviado e extrai automaticamente
        tokens numéricos de 6 dígitos (ativação / reset).
        """

        match = re.search(r"\b\d{6}\b", text_body)
        token = match.group() if match else None

        self.sent_emails.append(
            {
                "to": to,
                "subject": subject,
                "html": html_body,
                "text": text_body,
                "token": token,  # 👈 token extraído para uso nos testes
            }
        )

    # ----------------------------------------
    # Helpers para testes
    # ----------------------------------------
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
