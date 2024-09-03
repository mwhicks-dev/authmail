from abc import ABC, abstractmethod

from schema import MessageDto

class IMailHandler(ABC):

    @abstractmethod
    def send_email(self, dto: MessageDto) -> None:
        pass