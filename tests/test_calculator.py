import pytest

from expense_tracker.calculator import (
    add_expense,
    filter_by_category,
    filter_by_month,
    total,
    totals_by_category,
)


def make_sample():
    expenses = []
    add_expense(expenses, 10.00, "food", "Lunch", "2026-11-01")
    add_expense(expenses, 5.50, "transport", "Bus", "2026-11-02")
    add_expense(expenses, 20.00, "food", "Dinner", "2026-10-30")
    return expenses


def test_add_expense_assigns_incrementing_ids():
    expenses = make_sample()
    assert [e.id for e in expenses] == [1, 2, 3]


def test_add_expense_rejects_non_positive_amount():
    with pytest.raises(ValueError):
        add_expense([], 0, "food", "Nothing")
    with pytest.raises(ValueError):
        add_expense([], -5, "food", "Negative")


def test_add_expense_rejects_unknown_category():
    with pytest.raises(ValueError):
        add_expense([], 5, "crypto", "Coins")


def test_add_expense_rejects_invalid_or_noncanonical_date():
    for value in ("2026-02-30", "2026-2-03", "not-a-date"):
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            add_expense([], 5, "food", "Lunch", value)


def test_total():
    assert total(make_sample()) == 35.50


def test_totals_by_category():
    assert totals_by_category(make_sample()) == {"food": 30.0, "transport": 5.5}


def test_filter_by_category():
    assert len(filter_by_category(make_sample(), "food")) == 2


def test_filter_by_month():
    assert len(filter_by_month(make_sample(), "2026-11")) == 2
