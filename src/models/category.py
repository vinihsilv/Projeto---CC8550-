from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str
    user_id: int
