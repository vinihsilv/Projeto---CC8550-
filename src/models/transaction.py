from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    id: int | None
    amount: float
    type: str
    date: datetime
    category_id: int | None
    description: str | None
    user_id: int
