import csv
from typing import List, Dict

GRAY = "\033[90m"
RESET = "\033[0m"

TAX_RATE = 0.0825

TOP_GAMES = {
    'Clash of Clans': [
        'Clash of Clans',
        'Gold Pass',
        'Chest of Gems',
    ],
    'Hearthstone': [
        'Hearthstone',
    ],
    'Clash Royale': [
        'Clash Royale',
        'Pass Royale',
    ],
    'Pokémon GO': [
        'Pokémon GO',
        'PokéCoins',
        'Poke Genie',
    ],
    'Pixel Starships': [
        'Pixel Starships',
        'One Month Membership (Automatic Renewal)',
        'Bank of Starbux',
    ],
    'SimCity BuildIt': [
        'SimCity BuildIt',
    ],
    'Mr Love': [
        'Mr Love',
        '$0.99 Sale',
        '$4.99 Sale',
        '$12.99 Sale',
        '100 Gem',
        '310 Gem',
        '900 Gem',
        '6300 Gem',
        'Victor -',
        'Gavin -',
        'Kiro -',
        'Lucien -',
        '7-Day Pack',
        'Grand Stamina Pack',
        'Privilege Pack',
        'Privilege Growth Pack',
        'The Other Mrs',
    ],
}

OTHER_GAMES = [
    '1945 - Airplane',
    'A Dark Room',
    'Ball Sort Puzzle',
    'Beginner\'s Pack',
    'Biz Builder Delux',
    'Bit City',
    'Blip Blup',
    'Cake Sort Puzzle',
    'Cat Game',
    'Compulsive',
    'Dragon City',
    'Euclidean Lands',
    'Episode - Choose Your Story',
    'Expansion',
    'Flow Free',
    'Flow Free',
    'Florence',
    'Heads Up',
    'Harry Potter: Wizards Unite',
    'HPWU',
    'King of Kong',
    'Kingdom Rush Frontiers',
    'LIMBO',
    'Last Shelter',
    'Minecraft',
    'Monument Valley',
    'Neo Monsters',
    'Pocket Build',
    'Pocket City',
    'Plague Inc',
    'Pokémon Duel',
    'Race for the Galaxy',
    'Rent Please',
    'Silicon Valley : Billionaire, Essential Package',
    'Stardew Valley',
    'Sudoku.com',
    'Tamagotchi Classic',
    'The Room',
    'Transistor',
    'Trivia Crack',
    'UniWar',
    'Wanted',
    'Westworld',
    'World Cruise Story',
    'projekt',
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
