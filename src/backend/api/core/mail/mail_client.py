from abc import ABC, abstractmethod


class MailClient(ABC):

    @abstractmethod
    def send(
        self,
        to: str,
        subject: str,
        text: str,
        html: str,
    ) -> None:
        pass
