from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Purchase:
    store: str
    item: str
    price: float
    purchased_at: datetime | None
    subject: str | None = None

    def day_iso(self) -> str:
        """Return YYYY-MM-DD (in the email header's timezone) or empty string."""
        if self.purchased_at is None:
            return ""
        return self.purchased_at.strftime("%Y-%m-%d")

    def dedupe_key(self) -> tuple[str, str, float, str]:
        """A conservative key for de-duplicating obvious duplicates."""
        return (self.store, self.item, self.price, self.day_iso())
