import re
from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup, Tag

from PurchasedItem import PurchasedItem


class MessageContent(ABC):
    def __init__(self, store_name: str, subject: str, date: str, html: str):
        self._store_name = store_name
        self._subject = subject
        self._date = date
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')
    
    @abstractmethod
    def get_purchases(self) -> List[PurchasedItem]:
        pass
    
    def _make_purchased_item(self, item_elem: Tag, price_elem: Tag):
        price_elem_str = price_elem.text.strip()
        price_matches = re.findall(r'\$\d+\.\d{2}', price_elem_str)
        
        if len(price_matches) != 1:
            print(
                f'[{self._store_name}] oops! could not parse price from "{price_elem_str}"'
            )
            return None
        
        price = float(price_matches[0].replace('$', ''))
        
        return PurchasedItem(
            self._store_name,
            item_elem.text.strip(),
            price,
            self._date
        )


class AppleMessageContent(MessageContent):
    def get_purchases(self) -> List[PurchasedItem]:
        item_cells = self._soup.find_all(
            'td',
            class_='item-cell aapl-mobile-cell'
        )
        price_cells = self._soup.find_all(
            'td',
            class_='price-cell aapl-mobile-cell'
        )
        
        if len(item_cells) == 0 or len(price_cells) == 0:
            print(
                f'[{self._store_name}] oops! no items found for "{self._subject}" on {self._date}'
            )
            return []
        if len(item_cells) != len(price_cells):
            print(
                f'[{self._store_name}] oops! item_cells and price_cells have different lengths for "{self._subject}" on {self._date}'
            )
            return []
        
        purchases = []
        
        for i in range(len(item_cells)):
            p = self._make_purchased_item(
                item_cells[i].find('span', class_='title'),
                price_cells[i]
            )
            purchases.append(p) if p is not None else None
        
        return purchases


class GPlayMessageContent(MessageContent):
    def get_purchases(self) -> List[PurchasedItem]:
        item_rows = self._soup.find_all('tr', {'itemprop': 'acceptedOffer'})
        
        purchases = []
        
        for row in item_rows:
            p = self._make_purchased_item(
                row.find('span', {'itemprop': 'name'}),
                row.find('span', {'itemprop': 'price'})
            )
            purchases.append(p) if p is not None else None
        
        return purchases
