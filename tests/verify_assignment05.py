"""Dependency-free verification for Assignment 05 mitigations and core behavior."""

import csv
import io
import json

from expense_tracker.calculator import add_expense, filter_by_month, total
from expense_tracker.reports import render_report


def main():
    checks = 0
    expenses = []
    add_expense(expenses, 4.75, "food", "Lunch", "2026-11-20")
    assert expenses[0].id == 1
    checks += 1

    for invalid_date in ("2026-02-30", "2026-2-03", "not-a-date"):
        try:
            add_expense([], 1, "food", "Bad date", invalid_date)
        except ValueError:
            checks += 1
        else:
            raise AssertionError(f"accepted invalid date {invalid_date!r}")

    special = 'Lunch, "special"\nwith note'
    add_expense(expenses, 3.25, "food", special, "2026-11-21")
    rows = list(csv.reader(io.StringIO(render_report(expenses, "csv"))))
    assert rows[2][3] == special
    checks += 1
    assert json.loads(render_report(expenses, "json"))["total"] == 8.0
    checks += 1
    assert len(filter_by_month(expenses, "2026-11")) == 2 and total(expenses) == 8.0
    checks += 1

    print(f"PASS: {checks} standard-library verification checks")


if __name__ == "__main__":
    main()
