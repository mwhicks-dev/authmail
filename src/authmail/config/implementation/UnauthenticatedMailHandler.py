import json

from typing import Any
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

from behavior import IMailHandler
from schema import MessageDto

class UnauthenticatedMailHandler(IMailHandler):
    """
    No additional dependencies required.
    """

    _config: dict[str, Any]

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

    def send_email(self, dto: MessageDto) -> None:
        # use smtp to send email
        sender = self._config['smtp']['username']

        msg = MIMEText(f"Sender: {dto.sender}\n\n{dto.body}", "plain")
        msg['Subject'] = f"Message from {self._config['app_name']}"
        msg['From'] = sender

        conn = self._construct_smtp()
        conn.set_debuglevel(0)
        conn.sendmail(sender, [dto.recipients], msg.as_string())
        conn.quit()