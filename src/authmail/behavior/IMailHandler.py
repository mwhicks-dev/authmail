from abc import ABC, abstractmethod

from schema import MessageDto

class IMailHandler(ABC):

    @abstractmethod
    def send_email(dto: MessageDto) -> None:
        pass