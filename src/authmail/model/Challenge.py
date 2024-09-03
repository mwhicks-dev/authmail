from uuid import UUID
from datetime import datetime

class Challenge:
    id: UUID
    created_time: datetime
    email: str
    response: str