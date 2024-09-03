from abc import ABC, abstractmethod

from authmail.schema import EmailDto, ChallengeDto, ResponseDto

class IChallengeHandler(ABC):

    @abstractmethod
    def create_challenge(self, dto: EmailDto) -> ChallengeDto:
        pass

    @abstractmethod
    def handle_response(self, dto: ResponseDto) -> None:
        pass