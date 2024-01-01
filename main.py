import mailbox

from MobileStoreEmailManager import MobileStoreEmailManager


def main():
    apple = MobileStoreEmailManager(
        'apple', 'Your receipt from Apple',
        'app_store.mbox'
    )
    gplay = MobileStoreEmailManager(
        'gplay', 'Your Google Play Order Receipt',
        'gplay_store.mbox'
    )
    
    # Load the App Store or GPlay Store receipt emails
    if apple.mbox_pre_exists and gplay.mbox_pre_exists:
        print(
            'apple and gplay already exist. skipping loading all_emails.mbox...'
        )
    else:
        print('loading all_emails.mbox...')
        mbox = mailbox.mbox('all_emails.mbox')
        
        print('looking through all emails...')
        # Check to see if the message is from apple or gplay store,
        # and add it to the store's mbox file.
        for message in mbox:
            if not apple.mbox_pre_exists:
                apple.add_message(message)
            if not gplay.mbox_pre_exists:
                gplay.add_message(message)
        
        # Done using the all_emails mbox. Close it.
        mbox.close()
    
    # Now we can try to extract purchases from the emails
    
    
    # Done using apple/gplay mboxes. Close them.
    apple.close_mbox()
    gplay.close_mbox()


if __name__ == '__main__':
    main()
