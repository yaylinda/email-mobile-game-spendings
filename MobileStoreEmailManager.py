import mailbox
import os
from typing import List

import PurchasedItem
from MessageContent import MessageContent, AppleMessageContent, \
    GPlayMessageContent
from common import print_warning


class MobileStoreEmailManager:
    def __init__(
        self,
        store_name: str,
        email_subject_prefix: str,
        mbox_file: str
    ):
        self._store_name = store_name
        self._email_subject_prefix = email_subject_prefix
        self._mbox_file = mbox_file
        self._message_contents: List[MessageContent] = []
        
        if os.path.exists(mbox_file):
            # If mbox already exists, we won't try to add messages to it.
            self._mbox_pre_exists = True
        else:
            self._mbox_pre_exists = False
        
        # Create the mbox object
        self._mbox = mailbox.mbox(mbox_file)
        self._load_all()
        
        print(
            f'[{store_name}] initialized! pre-exists={self._mbox_pre_exists}, loaded {len(self._mbox)} messages'
        )
    
    @property
    def mbox_pre_exists(self):
        return self._mbox_pre_exists
    
    def add_message(self, message: mailbox.Message):
        if self._mbox_pre_exists:
            return
        
        subject = message.get('Subject', '')
        
        if not isinstance(subject, str):
            subject = str(subject)
        
        if subject.startswith(self._email_subject_prefix):
            self._mbox.add(message)
            self._add_message_content(message)
    
    def extract_purchases(self) -> List[PurchasedItem]:
        purchases: List[PurchasedItem] = []
        
        for msg in self._message_contents:
            purchases.extend(msg.get_purchases())
        
        print(
            f'[{self._store_name}] got {len(purchases)} purchases across {len(self._message_contents)} messages'
        )
        return purchases
    
    def close_mbox(self):
        self._mbox.close()
    
    def _load_all(self):
        for message in self._mbox:
            self._add_message_content(message)
    
    def _add_message_content(self, message: mailbox.Message):
        subject = message.get('Subject', '')
        date = message.get('Date', '')
        
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == 'text/html':
                    html = part.get_payload(decode=True)
                    
                    match self._store_name:
                        case 'apple':
                            self._message_contents.append(
                                AppleMessageContent(
                                    self._store_name,
                                    subject,
                                    date,
                                    html
                                )
                            )
                        case 'gplay':
                            self._message_contents.append(
                                GPlayMessageContent(
                                    self._store_name,
                                    subject,
                                    date,
                                    html
                                )
                            )
                        case _:
                            print_warning(
                                self._store_name,
                                'unknown store name'
                            )
        else:
            print_warning(self._store_name, 'not a multipart message')
