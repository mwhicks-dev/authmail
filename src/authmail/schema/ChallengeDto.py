from uuid import UUID

from pydantic import BaseModel

class ChallengeDto(BaseModel):

    id: UUID