from abc import ABC, abstractmethod


class MessageContent(ABC):
    def __init__(self, store_name: str, subject: str, date: str, html: str):
        self._store_name = store_name
        self._subject = subject
        self._date = date
        self._html = html
    
    @abstractmethod
    def parse_html(self):
        pass


class AppleMessageContent(MessageContent):
    def parse_html(self):
        # Implementation here
        pass


class GPlayMessageContent(MessageContent):
    def parse_html(self):
        # Implementation here
        pass
