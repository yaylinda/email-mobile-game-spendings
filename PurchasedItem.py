class PurchasedItem:
    def __init__(
        self,
        store_name: str,
        item_name: str,
        price: str,
        purchased_date: str
    ):
        self.store_name = store_name
        self.item_name = item_name
        self.price = price
        self.purchased_date = purchased_date
        
    def __repr__(self):
        return f'Store Name: {self.store_name}, Item Name: {self.item_name}, Price: {self.price}, Purchase Date: {self.purchased_date}'
