import json

from .calculator import total, totals_by_category


def render_report(expenses, fmt):
    """Full list of expenses in the requested format."""
    if fmt == "text":
        lines = [
            f"{e.date}  {e.category:<10} {e.amount:>8.2f}  {e.description}"
            for e in expenses
        ]
        lines.append(f"TOTAL: {total(expenses):.2f}")
        return "\n".join(lines)
    elif fmt == "csv":
        lines = ["date,category,amount,description"]
        for e in expenses:
            lines.append(f"{e.date},{e.category},{e.amount:.2f},{e.description}")
        return "\n".join(lines)
    elif fmt == "json":
        return json.dumps(
            {"expenses": [e.to_dict() for e in expenses], "total": total(expenses)},
            indent=2,
        )
    else:
        raise ValueError(f"unsupported format: {fmt}")


def render_summary(expenses, fmt):
    """Totals per category in the requested format."""
    totals = totals_by_category(expenses)
    if fmt == "text":
        lines = [f"{cat:<10} {amount:>8.2f}" for cat, amount in totals.items()]
        lines.append(f"TOTAL: {total(expenses):.2f}")
        return "\n".join(lines)
    elif fmt == "csv":
        lines = ["category,total"]
        for cat, amount in totals.items():
            lines.append(f"{cat},{amount:.2f}")
        return "\n".join(lines)
    elif fmt == "json":
        return json.dumps({"by_category": totals, "total": total(expenses)}, indent=2)
    else:
        raise ValueError(f"unsupported format: {fmt}")
