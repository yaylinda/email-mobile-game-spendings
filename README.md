# email-mobile-game-spendings
Generate a spending dataset from App Store / Google Play receipt emails.

This project parses exported email archives (in `.mbox` format), extracts purchases from receipt emails, and writes a normalized `data.csv` you can analyze/plot.

## Privacy / safety
- Your `.mbox` files contain private email content. Keep them local.
- This repo ignores `*.mbox` and `data/` by default via `.gitignore`.

## Setup (uv)
1) Install `uv` (recommended):
```bash
brew install uv
```
2) Install dependencies:
```bash
uv sync --dev
```

Optional (only needed for plotting):
```bash
uv sync --extra plot
```

## Generate the dataset (CSV)
Export your emails into one or more `.mbox` files (Apple receipts, Google Play receipts, or a combined mailbox).

Then run:
```bash
uv run email-mobile-game-spendings build --mbox /path/to/your.mbox --out data.csv
```

Multiple mboxes are supported:
```bash
uv run email-mobile-game-spendings build \
  --mbox /path/to/app_store.mbox \
  --mbox /path/to/gplay_store.mbox \
  --out data.csv \
  --dedupe
```

Output schema:
- `store`: `apple` or `gplay`
- `date`: `YYYY-MM-DD` (from the email Date header)
- `item`: item/app name
- `category`: derived from keyword rules
- `price`: pre-tax price
- `price_with_tax`: computed using a fixed tax rate

## Plot
Plotting requires the optional dependencies (`pandas` + `matplotlib`). Install them via:
```bash
uv sync --extra plot
```

Then:
```bash
uv run email-mobile-game-spendings plot --csv data.csv --out plot.png
```
Add `--show` to open an interactive window.

## Categorization rules
Keyword-based categorization lives in:
- `src/email_mobile_game_spendings/categorize.py`

This is intentionally simple for now; we can evolve it once you’ve exported your mbox and we decide which receipt emails to include/exclude.

## Legacy scripts
The repo originally started as a few one-off scripts at the repo root. The supported interface going forward is the CLI:
- `email-mobile-game-spendings build ...`
- `email-mobile-game-spendings plot ...`
