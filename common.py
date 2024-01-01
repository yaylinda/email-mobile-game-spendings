import csv
from typing import List, Dict

GRAY = "\033[90m"
RESET = "\033[0m"

TAX_RATE = 0.0825

KNOWN_GAMES = [
    'Clash of Clans',
    'Hearthstone',
    'Clash Royale',
    'Pokemon Go',
    'Pixel Starships',
    'SimCity BuildIt',
    'Mr Love',
]

COLUMNS = [
    'store',
    'date',
    'item',
    'category',
    'price',
    'price_with_tax'
]


def print_warning(context: str, message: str) -> None:
    print(f'{GRAY}[⚠️][{context}] oops! {message}{RESET}')


def write_csv(
    filename: str,
    columns: List[str],
    rows: List[Dict[str, str | float]]
) -> None:
    print(f"\nwriting {len(rows)} rows to {filename}...")
    
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    
    print('\t✅ done!')
