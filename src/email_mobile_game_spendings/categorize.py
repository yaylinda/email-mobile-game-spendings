from __future__ import annotations

TAX_RATE = 0.0825

TOP_GAMES: dict[str, list[str]] = {
    "Clash of Clans": [
        "Clash of Clans",
        "Gold Pass",
        "Chest of Gems",
    ],
    "Hearthstone": [
        "Hearthstone",
    ],
    "Clash Royale": [
        "Clash Royale",
        "Pass Royale",
    ],
    "Pokémon GO": [
        "Pokémon GO",
        "PokéCoins",
        "Poke Genie",
    ],
    "Pixel Starships": [
        "Pixel Starships",
        "One Month Membership (Automatic Renewal)",
        "Bank of Starbux",
    ],
    "SimCity BuildIt": [
        "SimCity BuildIt",
    ],
    "Mr Love": [
        "Mr Love",
        "$0.99 Sale",
        "$4.99 Sale",
        "$12.99 Sale",
        "100 Gem",
        "310 Gem",
        "900 Gem",
        "6300 Gem",
        "Victor -",
        "Gavin -",
        "Kiro -",
        "Lucien -",
        "7-Day Pack",
        "Grand Stamina Pack",
        "Privilege Pack",
        "Privilege Growth Pack",
        "The Other Mrs",
    ],
}

OTHER_GAMES: list[str] = [
    "1945 - Airplane",
    "94%",
    "A Dark Room",
    "Ball Sort Puzzle",
    "Beginner's Pack",
    "Biz Builder Delux",
    "Bit City",
    "Blip Blup",
    "Cake Sort Puzzle",
    "Cat Game",
    "Compulsive",
    "Dragon City",
    "Euclidean Lands",
    "Episode - Choose Your Story",
    "Expansion",
    "Flow Free",
    "Florence",
    "Heads Up",
    "Harry Potter: Wizards Unite",
    "HPWU",
    "King of Kong",
    "Kingdom Rush Frontiers",
    "LIMBO",
    "Last Shelter",
    "Minecraft",
    "Monument Valley",
    "Neo Monsters",
    "Pocket Build",
    "Pocket City",
    "Plague Inc",
    "Pokémon Duel",
    "Race for the Galaxy",
    "Rent Please",
    "Silicon Valley : Billionaire, Essential Package",
    "Stardew Valley",
    "Sudoku.com",
    "Tamagotchi Classic",
    "The Room",
    "Threes!",
    "Tiny Tower",
    "Transistor",
    "Trivia Crack",
    "UniWar",
    "Wanted",
    "Westworld",
    "World Cruise Story",
    "projekt",
]

NON_GAMES: list[str] = [
    "Apple",
    "Authenticator App",
    "Geekbench",
    "Google Play",
    "HBO NOW",
    "iCloud",
    "Life Cycle",
    "Reddit",
    "Spark Mail",
    "Weather",
    "YouTube",
]


def categorize_item(item_name: str) -> str:
    """Return a category string or empty string if uncategorized/non-game."""
    for category, keywords in TOP_GAMES.items():
        for keyword in keywords:
            if keyword in item_name:
                return category

    for keyword in OTHER_GAMES:
        if keyword in item_name:
            return "Other"

    for keyword in NON_GAMES:
        if keyword in item_name:
            return ""

    return ""
