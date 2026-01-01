from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .extractors import extract_apple_purchases, extract_gplay_purchases
from .mbox import extract_best_html, iter_mbox_messages, parse_email_datetime
from .models import Purchase


@dataclass(slots=True)
class ExtractionStats:
    messages_total: int = 0
    messages_with_html: int = 0
    purchases_total: int = 0
    purchases_by_store: Counter[str] | None = None

    def __post_init__(self) -> None:
        if self.purchases_by_store is None:
            self.purchases_by_store = Counter()


def extract_purchases_from_mboxes(
    mbox_paths: Iterable[str | Path],
    *,
    dedupe: bool = False,
    verbose: bool = False,
) -> tuple[list[Purchase], ExtractionStats]:
    purchases: list[Purchase] = []
    stats = ExtractionStats()

    seen: set[tuple[str, str, float, str]] = set()

    for mbox_path in mbox_paths:
        for msg in iter_mbox_messages(mbox_path):
            stats.messages_total += 1

            subject = msg.get("Subject", "")
            if not isinstance(subject, str):
                subject = str(subject)

            purchased_at = parse_email_datetime(msg.get("Date"))
            html = extract_best_html(msg)
            if not html:
                continue

            stats.messages_with_html += 1

            extracted: list[Purchase] = []
            extracted.extend(
                extract_apple_purchases(html, purchased_at=purchased_at, subject=subject)
            )
            extracted.extend(
                extract_gplay_purchases(html, purchased_at=purchased_at, subject=subject)
            )

            if not extracted:
                continue

            for p in extracted:
                if dedupe:
                    key = p.dedupe_key()
                    if key in seen:
                        continue
                    seen.add(key)

                purchases.append(p)
                stats.purchases_total += 1
                stats.purchases_by_store[p.store] += 1

            if verbose and stats.messages_total % 500 == 0:
                # Keep it lightweight for large mboxes.
                print(
                    f"processed {stats.messages_total} messages → {stats.purchases_total} purchases"
                )

    return purchases, stats
