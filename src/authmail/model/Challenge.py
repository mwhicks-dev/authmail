from uuid import UUID
from datetime import datetime

class Challenge:
    id: UUID
    created_time: datetime
    email: str
    response: str

    def __lt__(self, other):
        return self.created_time < other.created_time