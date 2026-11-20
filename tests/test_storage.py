from expense_tracker.calculator import add_expense
from expense_tracker.storage import load_expenses, save_expenses


def test_load_missing_file_returns_empty_list(tmp_path):
    assert load_expenses(str(tmp_path / "nope.json")) == []


def test_save_then_load_roundtrip(tmp_path):
    path = str(tmp_path / "data.json")
    expenses = []
    add_expense(expenses, 12.5, "food", "Lunch", "2026-11-01")
    save_expenses(expenses, path)
    loaded = load_expenses(path)
    assert loaded == expenses
