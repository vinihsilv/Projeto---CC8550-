from dataclasses import dataclass


@dataclass
class Budget:
    id: int
    category_id: int
    month: int
    year: int
    limit_value: float
    user_id: int
