import imaplib
import email
from getpass import getpass
from email.header import decode_header

print("This program allows you to delete emails from your Gmail account.")

email_count = 0
username = input("E-mail Address: ")
password = getpass("E-mail Password: ")


imap = imaplib.IMAP4_SSL("imap.gmail.com")

imap.login(username, password)

imap.select('"[Gmail]/All Mail"', readonly=False)

# Print list of Inboxes and allow to choose which 
# inbox to remove emails from.
# for i in imap.list()[1]:
#     l = i.decode().split(' "/" ')
#     print(l[0] + " = " + l[1])

# inbox = input("Which inbox: ")
# imap.select(f"{inbox}", readonly=False)

sender = input("Sender's E-mail Address: ")

status, messages = imap.search(None, f'FROM "{sender}"')

msg_count = len(messages[0].split())

messages = messages[0].split(b' ')

def loadbar(iterator, total, prefix='', suffix='', decimals=1, length=50, fill='*'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iterator/float(total)))
    filledLen = int(length * iterator // total)
    bar = fill * filledLen + '-' * (length - filledLen)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="")
    if iterator == total:
        print()

response = None

while response not in ('y', 'n'):
    response = input("Display subject of each email being deleted?(y/n): ")
    if response == 'y':
        for mail in messages:
            _, msg = imap.fetch(mail, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    print("Deleting", subject)
            email_count+=1
            imap.store(mail, "+X-GM-LABELS", "\\Trash")
            # imap.select("[Gmail]/Trash")
            # imap.store("1:*", '+FLAGS', '\\Deleted')

    elif response == 'n':
        loadbar(email_count, msg_count, prefix=f'Deleting e-mails from {sender}', suffix='Complete', length=50)
        # print(f"Deleting e-mails from {sender}...")
        for mail in messages:
            _, msg = imap.fetch(mail, "(RFC822)")
            email_count+=1
            loadbar(email_count, msg_count, prefix=f'Deleting e-mails from {sender}', suffix='Complete', length=50)
            imap.store(mail, "+X-GM-LABELS", "\\Trash")
            # imap.select("[Gmail]/Trash")
            # imap.store("1:*", '+FLAGS', '\\Deleted')
    else:
        print("Please enter 'y' or 'n'.")
    break

print(f"{email_count} e-mails deleted.")

imap.expunge()
imap.close()
imap.logout()