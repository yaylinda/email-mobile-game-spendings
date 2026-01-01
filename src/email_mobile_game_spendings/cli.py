from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .csv_utils import write_csv
from .pipeline import extract_purchases_from_mboxes


def _cmd_build(args: argparse.Namespace) -> int:
    purchases, stats = extract_purchases_from_mboxes(
        args.mbox,
        dedupe=args.dedupe,
        verbose=args.verbose,
    )

    written = write_csv(args.out, purchases)

    print(f"\nmessages: {stats.messages_total} (html: {stats.messages_with_html})")
    print(f"purchases: {stats.purchases_total} ({dict(stats.purchases_by_store)})")
    print(f"\nwrote {written} rows → {args.out}")

    return 0


def _cmd_plot(args: argparse.Namespace) -> int:
    try:
        from .plotting import plot_spend_by_year
    except ImportError as e:
        raise SystemExit(
            "Plot dependencies are not installed. Install extras (recommended):\n"
            "  uv sync --extra plot\n\n"
            "Or install manually: pandas + matplotlib"
        ) from e

    plot_spend_by_year(args.csv, out_path=args.out, show=args.show)
    print(f"wrote plot → {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="email-mobile-game-spendings",
        description=(
            "Generate a spending dataset from App Store / Google Play receipt emails (mbox exports)."
        ),
    )

    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="Parse mbox file(s) and write data.csv")
    build.add_argument(
        "--mbox",
        action="append",
        required=True,
        help="Path to an exported .mbox file. Repeatable.",
    )
    build.add_argument(
        "--out",
        default="data.csv",
        help="Output CSV path (default: data.csv)",
    )
    build.add_argument(
        "--dedupe",
        action="store_true",
        help="De-duplicate obvious duplicates (same store, item, price, day)",
    )
    build.add_argument(
        "--verbose",
        action="store_true",
        help="Print lightweight progress for large mboxes",
    )
    build.set_defaults(func=_cmd_build)

    plot = sub.add_parser("plot", help="Generate plot.png from a data.csv")
    plot.add_argument(
        "--csv",
        default="data.csv",
        help="Input CSV path (default: data.csv)",
    )
    plot.add_argument(
        "--out",
        default="plot.png",
        help="Output image path (default: plot.png)",
    )
    plot.add_argument(
        "--show",
        action="store_true",
        help="Open a window to show the plot interactively",
    )
    plot.set_defaults(func=_cmd_plot)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Normalize file args a bit.
    if getattr(args, "mbox", None):
        args.mbox = [str(Path(p)) for p in args.mbox]

    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
