from pydantic import BaseModel

class MessageDto(BaseModel):

    sender: str
    recipients: list[str]
    body: str