from __future__ import annotations

import mailbox
from datetime import datetime, timezone
from email.message import Message
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterator

from .log import warn


def parse_email_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    try:
        dt = parsedate_to_datetime(value)
    except Exception:
        warn("mbox", f"could not parse Date header: {value!r}")
        return None

    if dt is None:
        warn("mbox", f"could not parse Date header: {value!r}")
        return None

    # Some emails may lack tzinfo; treat as UTC rather than crashing downstream.
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt


def _decode_bytes(data: bytes, charset: str | None) -> str:
    if charset:
        try:
            return data.decode(charset, errors="replace")
        except LookupError:
            # Unknown codec
            pass

    # Common fallbacks.
    for enc in ("utf-8", "latin-1"):
        try:
            return data.decode(enc, errors="replace")
        except Exception:
            continue

    # Last resort.
    return data.decode("utf-8", errors="replace")


def extract_best_html(message: Message) -> str | None:
    """Best-effort extraction of the primary HTML body for an email message."""

    def is_attachment(part: Message) -> bool:
        disp = part.get("Content-Disposition", "") or ""
        return "attachment" in disp.lower()

    html_candidates: list[str] = []

    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() != "text/html":
                continue
            if is_attachment(part):
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            charset = part.get_content_charset() or None
            html_candidates.append(_decode_bytes(payload, charset))
    else:
        if message.get_content_type() == "text/html":
            payload = message.get_payload(decode=True)
            if payload:
                charset = message.get_content_charset() or None
                html_candidates.append(_decode_bytes(payload, charset))

    if not html_candidates:
        return None

    # Prefer the largest HTML part (usually the real body vs a tiny snippet).
    return max(html_candidates, key=len)


def iter_mbox_messages(path: str | Path) -> Iterator[Message]:
    mbox_path = Path(path)
    if not mbox_path.exists():
        raise FileNotFoundError(str(mbox_path))

    mbox = mailbox.mbox(str(mbox_path), create=False)
    try:
        for message in mbox:
            yield message
    finally:
        mbox.close()
