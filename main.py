import mailbox

from MobileStoreEmailManager import MobileStoreEmailManager
from common import write_csv, COLUMNS


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
            '\nskipping loading all_emails.mbox...\n'
        )
    else:
        mbox = mailbox.mbox('all_emails.mbox')
        print('\nloading all_emails.mbox...\n')
        
        # Check to see if the message is from apple or gplay store,
        # and add it to the store's mbox file.
        for message in mbox:
            if not apple.mbox_pre_exists:
                apple.add_message(message)
            if not gplay.mbox_pre_exists:
                gplay.add_message(message)
        
        # Done using the all_emails mbox. Close it.
        mbox.close()
    
    # Done using apple/gplay mboxes. Close them.
    apple.close_mbox()
    gplay.close_mbox()
    
    # Now we can try to extract purchases from the emails
    apple_purchases = apple.extract_purchases()
    gplay_purchases = gplay.extract_purchases()
    
    # Export the data to csv
    rows = [p.normalize_to_dict() for p in apple_purchases + gplay_purchases]
    write_csv('data.csv', COLUMNS, rows)


if __name__ == '__main__':
    main()
