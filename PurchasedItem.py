from datetime import datetime
from typing import Dict

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


class PurchasedItem:
    def __init__(
        self,
        store_name: str,
        item_name: str,
        price: float,
        purchased_date: str
    ):
        self.store_name = store_name
        self.item_name = item_name
        self.price = price
        self.purchased_date = purchased_date.replace("(GMT)", "")
    
    def normalize_to_dict(self) -> Dict[str, str | float]:
        datum = {}
        
        for column in COLUMNS:
            match column:
                case 'store':
                    datum[column] = self.store_name
                case 'date':
                    parsed_date = datetime.strptime(
                        self.purchased_date,
                        '%a, %d %b %Y %H:%M:%S %z'
                        )
                    datum[column] = parsed_date.strftime('%Y-%m-%d')
                case 'item':
                    datum[column] = self.item_name
                case 'category':
                    datum[column] = self._get_item_category(self.item_name)
                case 'price':
                    datum[column] = self.price
                case 'price_with_tax':
                    datum[column] = round(self.price * (1 + TAX_RATE), 2)
                case _:
                    print('oops! unknown column:', column)
        
        return datum
    
    @staticmethod
    def _get_item_category(item_name: str) -> str:
        for g in KNOWN_GAMES:
            if g in item_name:
                return g
        return 'OTHER'
    
    def __repr__(self):
        return (
            f'PurchasedItem('
            f'\n\tstore={self.store_name}'
            f'\n\titem_name={self.item_name}'
            f'\n\tprice={self.price}'
            f'\n\tpurchased_date={self.purchased_date}'
            f'\n)'
        )
