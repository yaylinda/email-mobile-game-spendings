import mailbox
import os
from typing import List

from MessageContent import MessageContent, AppleMessageContent, \
    GPlayMessageContent


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
        
        # If mbox already exists, we won't try to add messages to it.
        if os.path.exists(mbox_file):
            self._mbox_exists = True
        else:
            self._mbox_exists = False
        
        # Create the mbox object
        self._mbox = mailbox.mbox(mbox_file)
        
        print(
            '[{}] initialized! exists={}'.format(store_name, self._mbox_exists)
        )
    
    @property
    def mbox_exists(self):
        return self._mbox_exists
    
    def add_message(self, message: mailbox.Message):
        """
        :param message: the mailbox.Message object to be added to the mailbox
        :return: None

        Adds a given mailbox.Message object to the mailbox if the mailbox exists.
        It also prints a log message indicating the store name and the date when the message was added.
        If the subject of the message does not start with the email subject prefix, the message will not be added.
        """
        if self._mbox_exists:
            return
        
        subject = message.get('Subject', '')
        date = message.get('Date', '')
        
        if not isinstance(subject, str):
            subject = str(subject)
        
        if subject.startswith(self._email_subject_prefix):
            self._mbox.add(message)
            print('[{}][{}] added msg'.format(self._store_name, date))
    
    def get_messages_content(self) -> List[MessageContent]:
        """
        Retrieves the content of messages in the mailbox.

        :return: A list of MessageContent objects representing the content of messages.
        """
        messages_content = []
        
        for message in self._mbox:
            subject = message.get('Subject', '')
            date = message.get('Date', '')
            
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type() == 'text/html':
                        html = part.get_payload(decode=True)
                        
                        match self._store_name:
                            case 'apple':
                                messages_content.append(
                                    AppleMessageContent(
                                        self._store_name,
                                        subject,
                                        date,
                                        html
                                    )
                                )
                            case 'gplay':
                                messages_content.append(
                                    GPlayMessageContent(
                                        self._store_name,
                                        subject,
                                        date,
                                        html
                                    )
                                )
                            case _:
                                print('[{}] oops! unknown store name'.format(self._store_name))
            else:
                print(
                    '[{}] oops! not a multipart message'.format(
                        self._store_name
                    )
                )
                
        return messages_content
    
    def close_mbox(self):
        self._mbox.close()
        print('[{}] closed'.format(self._store_name))
