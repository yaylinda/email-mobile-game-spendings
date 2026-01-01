from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .categorize import TAX_RATE, categorize_item
from .models import Purchase

CSV_HEADERS: list[str] = [
    "store",
    "date",
    "item",
    "category",
    "price",
    "price_with_tax",
]


def purchase_to_row(p: Purchase) -> dict[str, str | float]:
    category = categorize_item(p.item)
    return {
        "store": p.store,
        "date": p.day_iso(),
        "item": p.item,
        "category": category,
        "price": p.price,
        "price_with_tax": round(p.price * (1 + TAX_RATE), 2),
    }


def write_csv(path: str | Path, purchases: Iterable[Purchase]) -> int:
    out_path = Path(path)
    rows = [purchase_to_row(p) for p in purchases]

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)
