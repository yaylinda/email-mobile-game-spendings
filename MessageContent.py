class MessageContent:
    def __init__(self, store_name: str, subject: str, date: str, html: str):
        self._store_name = store_name
        self._subject = subject
        self._date = date
        self._html = html
