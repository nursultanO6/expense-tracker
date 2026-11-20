from dataclasses import dataclass, asdict

CATEGORIES = ("food", "transport", "rent", "fun", "other")


@dataclass
class Expense:
    id: int
    amount: float
    category: str
    description: str
    date: str  # ISO format: YYYY-MM-DD

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
