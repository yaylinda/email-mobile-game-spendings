from datetime import datetime
from typing import Dict

from common import COLUMNS, TAX_RATE, TOP_GAMES, OTHER_GAMES, print_warning


class PurchasedItem:
    def __init__(
        self,
        store_name: str,
        item_name: str,
        price: float,
        date: str
    ):
        self._store_name = store_name
        self._item_name = item_name
        self._price = price
        self._date = date.replace("(GMT)", "").strip()
    
    def normalize_to_dict(self) -> Dict[str, str | float]:
        datum = {}
        
        for column in COLUMNS:
            match column:
                case 'store':
                    datum[column] = self._store_name
                case 'date':
                    parsed_date = datetime.strptime(
                        self._date,
                        '%a, %d %b %Y %H:%M:%S %z'
                    )
                    datum[column] = parsed_date.strftime('%Y-%m-%d')
                case 'item':
                    datum[column] = self._item_name
                case 'category':
                    datum[column] = self._get_item_category()
                case 'price':
                    datum[column] = self._price
                case 'price_with_tax':
                    datum[column] = round(self._price * (1 + TAX_RATE), 2)
                case _:
                    print('oops! unknown column:', column)
        
        return datum
    
    def _get_item_category(self) -> str:
        for category in TOP_GAMES:
            for keyword in TOP_GAMES[category]:
                if keyword in self._item_name:
                    return category
        
        for keyword in OTHER_GAMES:
            if keyword in self._item_name:
                return "Other"
        
        print_warning(self._store_name, f'"{self._item_name}" did not match any games')
        return ""
    
    def __repr__(self):
        return (
            f'PurchasedItem('
            f'\n\tstore={self._store_name}'
            f'\n\titem_name={self._item_name}'
            f'\n\tprice={self._price}'
            f'\n\tpurchased_date={self._date}'
            f'\n)'
        )
