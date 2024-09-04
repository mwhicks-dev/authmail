from uuid import UUID

from pydantic import BaseModel

class ResponseDto(BaseModel):

    id: UUID
    email: str
    response: str