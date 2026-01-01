from __future__ import annotations

import sys

_GRAY = "\033[90m"
_RESET = "\033[0m"


def warn(context: str, message: str) -> None:
    sys.stderr.write(f"{_GRAY}[warn][{context}] {message}{_RESET}\n")
