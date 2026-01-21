from typing import List, Dict


class MailClientMock:
    def __init__(self):
        self.sent_emails: List[Dict[str, str]] = []

    def send_email(
        self,
        *,
        to: str,
        subject: str,
        text: str,
        html: str,
    ) -> None:
        self.sent_emails.append(
            {
                "to": to,
                "subject": subject,
                "text": text,
                "html": html,
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
