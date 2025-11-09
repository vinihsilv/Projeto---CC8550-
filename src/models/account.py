# src/models/account.py
from dataclasses import dataclass


@dataclass
class Account:
    id: int | None
    name: str
    balance: float
    user_id: int
