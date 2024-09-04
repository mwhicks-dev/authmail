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
    """
    This IChallengeHandler implementation only uses the Python standard 
    library, but will require that you add a 'challenge_lifetime' member to 
    config.json which denotes how many seconds a challenge is valid for.

    config.json:
    ```json
    {
        ... ,
        "challenge_lifetime" : 600
    }
    ```

    MemoryChallengeHandler is constructed component-style with an 
    IResponseGenerator of your choice. This should be done in behavior.py, for 
    instance:

    ```python
    challenge_handler: IChallengeHandler = MemoryChallengeHandler(RandomIntResponseGenerator(6))
    ```
    """

    _config: dict[str, Any]
    _instance: dict[UUID, Challenge] = {}
    _sort: list[Challenge] = []
    _response_generator: IResponseGenerator

    def _construct_smtp(self) -> SMTP_SSL:
        smtp = SMTP_SSL()
        smtp._host = self._config['smtp']['host']  # see https://github.com/python/cpython/issues/80275

        # Connect to mail server
        smtp.connect(self._config['smtp']['host'], 
                     self._config['smtp']['port'])
        
        # Log in using specified account
        smtp.login(self._config['smtp']['username'], 
                   self._config['smtp']['password'])
        
        return smtp
    
    def _remove_old_challenges(self) -> None:
        lifetime = self._config['challenge_lifetime']
        while len(self._sort) > 0:
            self._sort.sort()
            first_age = (datetime.now() - self._sort[0].created_time).seconds
            if first_age > lifetime:
                try:
                    del self._instance[self._sort[0].id]
                except KeyError:
                    pass
                del self._sort[0]
            else:
                break

    def __init__(self, response_generator: IResponseGenerator):
        self._response_generator = response_generator
        with open("config/config.json", "r") as fp:
            self._config = json.load(fp)

    def create_challenge(self, dto: EmailDto) -> ChallengeDto:
        self._remove_old_challenges()

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

        self._sort.append(self._instance[uuid])

        output = ChallengeDto(id=uuid)

        return output

    def handle_response(self, dto: ResponseDto) -> None:
        self._remove_old_challenges()

        if dto.id not in self._instance.keys():
            raise InvalidChallengeException()
        elif dto.email != self._instance[dto.id].email:
            del self._instance[dto.id]
            raise InvalidChallengeException()
        elif dto.response != self._instance[dto.id].response:
            del self._instance[dto.id]
            raise InvalidResponseException()
        
        del self._instance[dto.id]
        
