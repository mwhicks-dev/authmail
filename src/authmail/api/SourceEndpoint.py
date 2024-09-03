from authmail.schema import EmailDto, ChallengeDto, ResponseDto, MessageDto
from authmail.behavior import IChallengeHandler, IMailHandler
from .Endpoint import Endpoint

class SourceEndpoint(Endpoint):

    _challenge_handler: IChallengeHandler
    _mail_handler: IMailHandler

    def __init__(self, challenge_handler: IChallengeHandler, 
                 mail_handler: IMailHandler):
        self._challenge_handler = challenge_handler
        self._mail_handler = mail_handler
    
    def submit_email(self, dto: EmailDto) -> ChallengeDto:
        return self._challenge_handler.create_challenge(dto)
    
    def submit_response(self, dto: ResponseDto) -> None:
        return self._challenge_handler.handle_response(dto)

    def send_email(self, dto: MessageDto) -> None:
        return self._mail_handler.send_email(dto)