import json
import csv
import io

import pytest

from expense_tracker.calculator import add_expense
from expense_tracker.reports import render_report, render_summary


def sample():
    expenses = []
    add_expense(expenses, 10, "food", "Lunch", "2026-11-01")
    add_expense(expenses, 5, "transport", "Bus", "2026-11-02")
    return expenses


def test_text_report_contains_total():
    assert "TOTAL: 15.00" in render_report(sample(), "text")


def test_csv_report_has_header_and_rows():
    lines = render_report(sample(), "csv").splitlines()
    assert lines[0] == "date,category,amount,description"
    assert len(lines) == 3


def test_csv_report_escapes_special_description_characters():
    expenses = []
    add_expense(expenses, 3.25, "food", 'Lunch, "special"\nwith note', "2026-11-03")
    rows = list(csv.reader(io.StringIO(render_report(expenses, "csv"))))
    assert rows[0] == ["date", "category", "amount", "description"]
    assert rows[1] == ["2026-11-03", "food", "3.25", 'Lunch, "special"\nwith note']


def test_json_report_is_valid_json():
    data = json.loads(render_report(sample(), "json"))
    assert data["total"] == 15


def test_summary_json():
    data = json.loads(render_summary(sample(), "json"))
    assert data["by_category"] == {"food": 10, "transport": 5}


def test_unsupported_format_raises():
    with pytest.raises(ValueError):
        render_report(sample(), "xml")
    with pytest.raises(ValueError):
        render_summary(sample(), "xml")
