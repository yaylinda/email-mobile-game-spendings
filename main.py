import mailbox

APP_STORE_SUBJECT = 'Your receipt from Apple'
GPLAY_STORE_SUBJECT = 'Your Google Play Order Receipt'


def main():
    # Load the mbox file
    mbox = mailbox.mbox('emails.mbox')

    num = 0
    app_store = []
    gplay_store = []

    for message in mbox:
        subject = message.get('subject', '')
        num += 1

        if not isinstance(subject, str):
            subject = str(subject)

        if APP_STORE_SUBJECT in subject:
            app_store.append(message)
            print('[#{}] {}'.format(num, subject))
        if GPLAY_STORE_SUBJECT in subject:
            gplay_store.append(message)
            print('[#{}] {}'.format(num, subject))

    print('got {} app_store emails'.format(len(app_store)))
    print('got {} gplay_store emails'.format(len(gplay_store)))


if __name__ == '__main__':
    main()