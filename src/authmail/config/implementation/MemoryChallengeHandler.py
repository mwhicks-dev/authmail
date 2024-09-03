import json

from typing import Any
from datetime import datetime
from uuid import uuid4, UUID
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

from behavior import IChallengeHandler, IResponseGenerator
from model import Challenge, InvalidChallengeException, InvalidResponseException
from schema import EmailDto, ChallengeDto, ResponseDto

class MemoryChallengeHandler(IChallengeHandler):

    _config: dict[str, Any]
    _instance: dict[UUID, Challenge] = {}
    _response_generator: IResponseGenerator
    _app_name: str

    def _construct_smtp(self) -> SMTP_SSL:
        smtp = SMTP_SSL()
        smtp._host = self._config['smtp']['host']

        # Connect to mail server
        smtp.connect(self._config['smtp']['host'], 
                     self._config['smtp']['port'])
        
        # Log in using specified account
        smtp.login(self._config['smtp']['username'], 
                   self._config['smtp']['password'])
        
        return smtp

    def __init__(self, app_name: str, response_generator: IResponseGenerator):
        self._response_generator = response_generator
        with open("config/config.json", "r") as fp:
            self._config = json.load(fp)
        self._app_name = app_name

    def create_challenge(self, dto: EmailDto) -> ChallengeDto:
        # generate challenge/response
        response = self._response_generator.generate_response()

        # get unique UUID
        uuid = uuid4()
        while uuid in self._instance.keys():
            uuid = uuid4()
        
        # create new challenge
        self._instance[uuid] = Challenge()
        self._instance[uuid].id = uuid
        self._instance[uuid].email = dto.email
        self._instance[uuid].response = response
        self._instance[uuid].created_time = datetime.now()
        
        # use smtp to send email
        sender = self._config['smtp']['username']

        msg = MIMEText(f"Your one-time password: {response}", "plain")
        msg['Subject'] = f"One Time Password from {self._config['app_name']}"
        msg['From'] = sender

        conn = self._construct_smtp()
        conn.set_debuglevel(0)
        conn.sendmail(sender, [dto.email], msg.as_string())
        conn.quit()

        output = ChallengeDto(id=uuid)

        return output

    def handle_response(self, dto: ResponseDto) -> None:
        if dto.id not in self._instance.keys():
            raise InvalidChallengeException()
        elif dto.email != self._instance[dto.id].email:
            del self._instance[dto.id]
            raise InvalidChallengeException()
        elif dto.response != self._instance[dto.id].response:
            del self._instance[dto.id]
            raise InvalidResponseException()
        
        del self._instance[dto.id]
        
