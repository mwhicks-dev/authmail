import json
import httpx

from typing import Any
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

from fastapi import HTTPException

from behavior import IMailHandler
from schema import MessageDto

class PyAcctMailHandler(IMailHandler):
    """
    PyAcctMailHandler is an IMailHandler implementation that uses HTTP to 
    verify users via the [PyAcct](https://github.com/mwhicks-dev) software. As 
    such, PyAcct is a dependency (specifically with an attribute 'email') 
    externally.

    This implementation uses the Python `httpx` which should be added to 
    your requirements.txt and/or installed in your local development 
    environment. Also, you should add the 'pyacct_base_url' field to your 
    config.json, specifying where PyAcct is HTTP-accessible:

    ```json
    {
        "app_name" : "Your Application Display Name",
        "smtp" : {
            "host": "your.mail.server",
            "port": 993,
            "username": "some@email.address",
            "password": "email_address_pw"
        },
        "pyacct_base_uri": "http://pyacct.address:port/pyacct/2"
    }
    ```
    """

    _config: dict[str, Any]

    _pyacct_username: str
    _pyacct_password: str

    def __init__(self):
        with open("config/config.json", "r") as fp:
            self._config = json.load(fp)

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
    
    def _validate_sender(self, sender: str, token: str | None):
        # check for null token
        if token is None:
            raise HTTPException(status_code=401, detail="PyAcct token required")
        
        # attempt to read acount from token
        resp = httpx.get(
            f'{self._config["pyacct_base_uri"]}/account/', 
            headers={'token' : token}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail=resp.json()['detail'])
        account_id = resp.json()['id']

        # read account email from ID
        resp = httpx.get(
            f'{self._config["pyacct_base_uri"]}/account/{account_id}/email', 
            headers={'token' : token}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail=resp.json()['detail'])
        email = resp.json()['value']

        # verify email and sender match
        if email != sender:
            raise HTTPException(status_code=401, detail=f"Sender {sender} does not match with authenticated user's email {email}")

    def send_email(self, dto: MessageDto) -> None:
        sender = self._config['smtp']['username']
        self._validate_sender(sender=dto.sender, token=dto.authorization)

        # use smtp to send email
        msg = MIMEText(f"Sender: {dto.sender}\n\n{dto.body}", "plain")
        msg['Subject'] = f"Message from {self._config['app_name']}"
        msg['From'] = sender

        conn = self._construct_smtp()
        conn.set_debuglevel(0)
        for recipient in dto.recipients:
            conn.sendmail(sender, [recipient], msg.as_string())
        conn.quit()