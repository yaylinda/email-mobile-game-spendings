from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class MessageContent(ABC):
    def __init__(self, store_name: str, subject: str, date: str, html: str):
        self.store_name = store_name
        self.subject = subject
        self.date = date
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')
    
    @abstractmethod
    def parse_html(self):
        pass


class AppleMessageContent(MessageContent):
    def parse_html(self):
        # # Find the table with the class 'aapl-desktop-tbl'
        # tables = self.soup.find_all('table', class_='aapl-desktop-tbl')
        #
        # # Iterate through the tables to find the one with purchase details
        # for table in tables:
        #     rows = table.find_all('tr')
        #     for row in rows:
        #         # Assuming the item name and price are in separate cells
        #         cells = row.find_all('td')
        #         if len(cells) >= 2:
        #             item = cells[0].get_text(strip=True)
        #             price = cells[-1].get_text(strip=True)
        #             if item and price:
        #                 print(f"Item: {item}, Price: {price}")
        return


class GPlayMessageContent(MessageContent):
    def parse_html(self):
        # Implementation here
        return
