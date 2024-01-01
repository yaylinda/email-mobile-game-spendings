import re
from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup, Tag

from PurchasedItem import PurchasedItem


class MessageContent(ABC):
    def __init__(self, store_name: str, subject: str, date: str, html: str):
        self.store_name = store_name
        self.subject = subject
        self.date = date
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')
    
    @abstractmethod
    def get_purchases(self) -> List[PurchasedItem]:
        pass


class AppleMessageContent(MessageContent):
    def get_purchases(self) -> List[PurchasedItem]:
        print('[{}] parsing purchases from html... "{}" on {}'.format(self.store_name, self.subject, self.date))
        
        item_cells = self.soup.find_all(
            'td',
            class_='item-cell aapl-mobile-cell'
            )
        price_cells = self.soup.find_all(
            'td',
            class_='price-cell aapl-mobile-cell'
            )
        
        if len(item_cells) == 0 or len(price_cells) == 0:
            print('\tno items found')
            return []
        if len(item_cells) != len(price_cells):
            print('\titem_cells and price_cells have different lengths')
            return []
        
        print('\tfound {} items'.format(len(item_cells)))
        
        purchases = []
        
        for i in range(len(item_cells)):
            item_elem: Tag = item_cells[i]
            item_name = item_elem.find('span', class_='title').text
            
            price_elem_str = price_cells[i].text
            prices = re.findall(r'\$\d+\.\d{2}', price_elem_str)
            if len(prices) != 1:
                print(
                    '\tfound {} prices for {}. expected 1'.format(
                        len(prices),
                        item_name
                        )
                    )
                continue
            
            purchases.append(
                PurchasedItem(self.store_name, item_name, prices[0], self.date)
            )
        
        return purchases


class GPlayMessageContent(MessageContent):
    def get_purchases(self) -> List[PurchasedItem]:
        # Implementation here
        return []
