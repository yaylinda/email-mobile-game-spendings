import mailbox
import os


class MobileStoreEmailManager:
    def __init__(self, store_name: str, email_subject: str, mbox_file: str):
        print('[{}] initing'.format(store_name))

        self._store_name = store_name
        self._email_subject = email_subject
        self._mbox_file = mbox_file

        # If mbox already exists, we won't try to add messages to it.
        if os.path.exists(mbox_file):
            self._mbox_exists = True
        else:
            self._mbox_exists = False

        # Create the mbox object
        self._mbox = mailbox.mbox(mbox_file)

    @property
    def mbox_exists(self):
        return self._mbox_exists

    def add_message(self, message: mailbox.Message):
        if self._mbox_exists:
            return

        subject = message.get('Subject', '')
        date = message.get('Date', '')

        if not isinstance(subject, str):
            subject = str(subject)

        if self._email_subject in subject:
            self._mbox.add(message)
            print('[{}][{}] added msg'.format(self._store_name, date))

    def parse_messages(self):
        for message in self._mbox:
            if message.is_multipart():
                for part in message.walk():
                    if (part.get_content_type() == 'text/plain'
                            or part.get_content_type() == 'text/html'):
                        print(part.get_payload())
            else:
                print(message.get_payload())

    def close_mbox(self):
        self._mbox.close()
        print('[{}] closed'.format(self._store_name))