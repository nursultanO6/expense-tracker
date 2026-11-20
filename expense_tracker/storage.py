import json
import os

from .models import Expense

DEFAULT_PATH = "expenses.json"


def load_expenses(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        data = json.load(f)
    return [Expense.from_dict(item) for item in data]


def save_expenses(expenses, path=DEFAULT_PATH):
    with open(path, "w") as f:
        json.dump([e.to_dict() for e in expenses], f, indent=2)


def next_id(expenses):
    return max((e.id for e in expenses), default=0) + 1
