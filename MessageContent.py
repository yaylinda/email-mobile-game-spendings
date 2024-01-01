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
        item_cells = self.soup.find_all(
            'td',
            class_='item-cell aapl-mobile-cell'
        )
        price_cells = self.soup.find_all(
            'td',
            class_='price-cell aapl-mobile-cell'
        )
        
        if len(item_cells) == 0 or len(price_cells) == 0:
            print(
                '[{}] oops! no items found for "{}" on {}'.format(
                    self.store_name,
                    self.subject,
                    self.date
                )
            )
            return []
        if len(item_cells) != len(price_cells):
            print(
                '[{}] oops! item_cells and price_cells have different lengths for "{}" on {}'.format(
                    self.store_name,
                    self.subject,
                    self.date
                )
            )
            return []
        
        purchases = []
        
        for i in range(len(item_cells)):
            item_elem: Tag = item_cells[i]
            item_name = item_elem.find('span', class_='title').text.strip()
            
            price_elem_str = price_cells[i].text.strip()
            prices = re.findall(r'\$\d+\.\d{2}', price_elem_str)
            if len(prices) != 1:
                print(
                    '[{}] oops! got {} prices for {}. expected 1'.format(
                        self.store_name,
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
        item_rows = self.soup.find_all('tr', {'itemprop': 'acceptedOffer'})
        
        purchases = []
        
        for row in item_rows:
            item_elem = row.find('span', {'itemprop': 'name'})
            item_name = item_elem.text.strip()
            
            price_elem = row.find('span', {'itemprop': 'price'})
            price = price_elem.text.strip()
            
            purchases.append(
                PurchasedItem(self.store_name, item_name, price, self.date)
                )
        
        return purchases
