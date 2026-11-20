from datetime import date as _date

from .models import CATEGORIES, Expense
from .storage import next_id


def add_expense(expenses, amount, category, description, date_str=None):
    """Create a new Expense, append it to `expenses` and return it."""
    if amount <= 0:
        raise ValueError("amount must be greater than 0")
    if category not in CATEGORIES:
        raise ValueError(f"unknown category: {category}")
    expense = Expense(
        id=next_id(expenses),
        amount=round(amount, 2),
        category=category,
        description=description,
        date=date_str or _date.today().isoformat(),
    )
    expenses.append(expense)
    return expense


def filter_by_category(expenses, category):
    return [e for e in expenses if e.category == category]


def filter_by_month(expenses, month):
    """`month` is a string like '2026-11'."""
    return [e for e in expenses if e.date.startswith(month)]


def total(expenses):
    return round(sum(e.amount for e in expenses), 2)


def totals_by_category(expenses):
    result = {}
    for e in expenses:
        result[e.category] = round(result.get(e.category, 0) + e.amount, 2)
    return result
