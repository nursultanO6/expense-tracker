# Expense Tracker CLI

A small command-line expense tracker written in Python (standard library only).
Expenses are stored in a local JSON file (`expenses.json` in the current directory).

## Requirements
- Python 3.9+
- pytest (for running tests)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
```bash
python -m expense_tracker add 12.50 food "Lunch at cafe"
python -m expense_tracker add 3.20 transport "Bus ticket" --date 2026-11-18
python -m expense_tracker list
python -m expense_tracker list --category food
python -m expense_tracker total
python -m expense_tracker total --month 2026-11
python -m expense_tracker report --format text
python -m expense_tracker report --format csv
python -m expense_tracker summary --format json
```

Categories: `food`, `transport`, `rent`, `fun`, `other`.

## Run tests
```bash
python -m pytest
```

## Project layout
```
expense_tracker/
  models.py       Expense dataclass and category list
  storage.py      load/save expenses to a JSON file
  calculator.py   add/filter/total logic
  reports.py      text/csv/json report and summary rendering
  cli.py          argparse command-line interface
tests/            pytest tests
```
