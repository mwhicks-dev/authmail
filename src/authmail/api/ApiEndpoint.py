import re

from fastapi import HTTPException

from schema import EmailDto, ChallengeDto, ResponseDto, MessageDto
from model import InvalidChallengeException, InvalidResponseException
from .Endpoint import Endpoint
from .SourceEndpoint import SourceEndpoint

class ApiEndpoint(Endpoint):

    base_path: str = "/authmail/1"

    _src: SourceEndpoint
    _regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    def _check(self, email):
        # ref: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

        if not re.fullmatch(self._regex, email):
            raise HTTPException(status_code=400, detail=f"Invalid email {email}")

    def __init__(self, src: SourceEndpoint):
        self._src = src

    def submit_email(self, dto: EmailDto) -> ChallengeDto:
        self._check(dto.email)

        return self._src.submit_email(dto)

    def submit_response(self, dto: ResponseDto) -> None:
        try:
            self._src.submit_response(dto)
        except InvalidChallengeException:
            raise HTTPException(status_code=404, detail=f"No such challenge; it may have expired")
        except InvalidResponseException:
            raise HTTPException(status_code=400, detail=f"Response does not match challenge; please request a new one")

    def send_email(self, dto: MessageDto) -> None:
        self._check(dto.sender)
        for recipient in dto.recipients:
            self._check(recipient)

        self._src.send_email(dto)