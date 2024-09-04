from pydantic import BaseModel

class EmailDto(BaseModel):

    email: str