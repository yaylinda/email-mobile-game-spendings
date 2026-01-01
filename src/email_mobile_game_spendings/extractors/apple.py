from __future__ import annotations

from datetime import datetime

from bs4 import BeautifulSoup

from ..log import warn
from ..models import Purchase
from .common import clean_text, parse_price_usd


def extract_purchases(
    html: str,
    *,
    purchased_at: datetime | None,
    subject: str | None = None,
) -> list[Purchase]:
    """Extract purchases from an Apple receipt email HTML body."""
    soup = BeautifulSoup(html, "lxml")

    item_cells = soup.find_all("td", class_="item-cell aapl-mobile-cell")
    price_cells = soup.find_all("td", class_="price-cell aapl-mobile-cell")

    if not item_cells or not price_cells:
        return []

    if len(item_cells) != len(price_cells):
        warn("apple", f"item/price cell count mismatch: {len(item_cells)} vs {len(price_cells)}")
        return []

    purchases: list[Purchase] = []

    for item_td, price_td in zip(item_cells, price_cells, strict=False):
        title = item_td.find("span", class_="title")
        if title is None:
            continue

        price = parse_price_usd(price_td.get_text(" ", strip=True), context="apple")
        if price is None:
            continue

        purchases.append(
            Purchase(
                store="apple",
                item=clean_text(title.get_text(" ", strip=True)),
                price=price,
                purchased_at=purchased_at,
                subject=subject,
            )
        )

    return purchases
