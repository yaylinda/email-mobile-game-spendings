from __future__ import annotations

from datetime import datetime

from bs4 import BeautifulSoup

from ..models import Purchase
from .common import clean_text, parse_price_usd


def extract_purchases(
    html: str,
    *,
    purchased_at: datetime | None,
    subject: str | None = None,
) -> list[Purchase]:
    """Extract purchases from a Google Play receipt email HTML body."""
    soup = BeautifulSoup(html, "lxml")

    item_rows = soup.find_all("tr", {"itemprop": "acceptedOffer"})
    if not item_rows:
        return []

    purchases: list[Purchase] = []

    for row in item_rows:
        name_elem = row.find("span", {"itemprop": "name"})
        price_elem = row.find("span", {"itemprop": "price"})

        if name_elem is None or price_elem is None:
            continue

        price = parse_price_usd(price_elem.get_text(" ", strip=True), context="gplay")
        if price is None:
            continue

        purchases.append(
            Purchase(
                store="gplay",
                item=clean_text(name_elem.get_text(" ", strip=True)),
                price=price,
                purchased_at=purchased_at,
                subject=subject,
            )
        )

    return purchases
