import argparse
import sys

from .calculator import (
    add_expense,
    filter_by_category,
    filter_by_month,
    total,
)
from .models import CATEGORIES
from .reports import render_report, render_summary
from .storage import DEFAULT_PATH, load_expenses, save_expenses


def build_parser():
    parser = argparse.ArgumentParser(prog="expense_tracker")
    parser.add_argument("--file", default=DEFAULT_PATH, help="path to JSON data file")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add an expense")
    p_add.add_argument("amount", type=float)
    p_add.add_argument("category", choices=CATEGORIES)
    p_add.add_argument("description")
    p_add.add_argument("--date", help="YYYY-MM-DD (default: today)")

    p_list = sub.add_parser("list", help="list expenses")
    p_list.add_argument("--category", choices=CATEGORIES)
    p_list.add_argument("--month", help="YYYY-MM")

    p_total = sub.add_parser("total", help="show total spent")
    p_total.add_argument("--category", choices=CATEGORIES)
    p_total.add_argument("--month", help="YYYY-MM")

    p_report = sub.add_parser("report", help="print full report")
    p_report.add_argument("--format", default="text", dest="fmt")

    p_summary = sub.add_parser("summary", help="print totals per category")
    p_summary.add_argument("--format", default="text", dest="fmt")

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    expenses = load_expenses(args.file)

    if args.command == "add":
        try:
            e = add_expense(expenses, args.amount, args.category, args.description, args.date)
        except ValueError as err:
            print(f"Error: {err}")
            sys.exit(1)
        save_expenses(expenses, args.file)
        print(f"Added #{e.id}: {e.amount:.2f} {e.category} - {e.description}")

    elif args.command == "list":
        items = expenses
        if args.category:
            items = filter_by_category(items, args.category)
        if args.month:
            items = filter_by_month(items, args.month)
        for e in items:
            print(f"#{e.id} {e.date} {e.category:<10} {e.amount:>8.2f}  {e.description}")

    elif args.command == "total":
        items = expenses
        if args.category:
            items = filter_by_category(items, args.category)
        if args.month:
            items = filter_by_month(items, args.month)
        print(f"Total: {total(items):.2f}")

    elif args.command == "report":
        try:
            print(render_report(expenses, args.fmt))
        except ValueError as err:
            print(f"Error: {err}")
            sys.exit(1)

    elif args.command == "summary":
        try:
            print(render_summary(expenses, args.fmt))
        except ValueError as err:
            print(f"Error: {err}")
            sys.exit(1)


if __name__ == "__main__":
    main()
