from __future__ import annotations

import re

from ..log import warn


def clean_text(value: str) -> str:
    return " ".join(value.split()).strip()


def parse_price_usd(text: str, *, context: str = "price") -> float | None:
    """Best-effort USD price parsing from receipt snippets."""
    s = clean_text(text)

    # $9.99, $ 9.99, US$9.99
    m = re.search(r"\b(?:US\$|\$)\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)\b", s)
    if m:
        return float(m.group(1).replace(",", ""))

    # USD 9.99
    m = re.search(r"\bUSD\s*([0-9]+(?:\.[0-9]{2})?)\b", s)
    if m:
        return float(m.group(1))

    # Fallback: any 0.00-like number
    m = re.search(r"\b([0-9]+\.[0-9]{2})\b", s)
    if m:
        return float(m.group(1))

    warn(context, f"could not parse price from: {s!r}")
    return None
