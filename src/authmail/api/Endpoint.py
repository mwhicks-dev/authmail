from abc import ABC, abstractmethod

from authmail.schema import EmailDto, ChallengeDto, ResponseDto, MessageDto

class Endpoint(ABC):

    @abstractmethod
    def submit_email(self, dto: EmailDto) -> ChallengeDto:
        pass

    @abstractmethod
    def submit_response(self, dto: ResponseDto) -> None:
        pass

    @abstractmethod
    def send_email(self, dto: MessageDto) -> None:
        pass