from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Expense:
    id: int
    category_id: int
    value: float
    date: datetime
    description: Optional[str] = None
