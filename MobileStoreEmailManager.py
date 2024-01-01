import base64
import mailbox
import os

from MessageContent import MessageContent


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
        if self._mbox_exists:
            return

        subject = message.get('Subject', '')
        date = message.get('Date', '')

        if not isinstance(subject, str):
            subject = str(subject)

        if subject.startswith(self._email_subject_prefix):
            self._mbox.add(message)
            print('[{}][{}] added msg'.format(self._store_name, date))

    def get_messages_content(self):
        messages_content = []

        for message in self._mbox:
            subject = message.get('Subject', '')
            date = message.get('Date', '')

            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type() == 'text/html':
                        html = part.get_payload(decode=True)
                        messages_content.append(
                            MessageContent(
                                self._store_name,
                                subject,
                                date,
                                html
                                )
                            )
            else:
                print(
                    '[{}] oops! not a multipart message'.format(
                        self._store_name
                        )
                    )

    def close_mbox(self):
        self._mbox.close()
        print('[{}] closed'.format(self._store_name))
