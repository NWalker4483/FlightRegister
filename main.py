import time
from itertools import chain
import email
import imaplib
import smtplib
from readair import Log

MY_NAME="Nile Walker"
MY_ADDRESS = 'nilezwalker@gmail.com'
PASSWORD = input('Enter the password for {}\n'.format(MY_ADDRESS))
MY_NUMBER='410-805-0012'
SUBJECT="Google Housing Request"
SERVER_ADDRESS="smtp.gmail.com"
PORT=587


# Restrict mail search. Be very specific.
# Machine should be very selective to receive messages.
criteria = {
    'FROM':    'yahoo@antonakis.co.uk',
    #S'SUBJECT': 'SPECIAL SUBJECT LINE',
    #'BODY':    'SECRET SIGNATURE',
}
uid_max = 0
def getBody(b):
    body = ""
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body = b.get_payload(decode=True)
    return body
def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()


mail = imaplib.IMAP4_SSL(SERVER_ADDRESS)
mail.login(MY_ADDRESS,PASSWORD)
mail.select('INBOX')

typ, data = mail.search(None, '(FROM "yahoo@antonakis.co.uk")')
mail_ids = data[0]
id_list = mail_ids.split()

for email_id in id_list:
    result, data = mail.fetch(email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
    msg=email.message_from_bytes(data[0][1])
    body = getBody(msg)
    body = body.decode("utf-8")
    body = "".join(body.split('\r'))
    Log(body)
mail.logout()

"""
# Keep checking messages ...
# I don't like using IDLE because Yahoo does not support it.
while 1:
    # Have to login/logout each time because that's the only way to get fresh results.

    server = imaplib.IMAP4_SSL(SERVER_ADDRESS)
    server.login(MY_ADDRESS,PASSWORD)
    server.select('INBOX')

    result, data = server.uid('search', None, search_string(uid_max, criteria))

    uids = [int(s) for s in data[0].split()]
    for uid in uids:
        # Have to check again because Gmail sometimes does not obey UID criterion.
        if uid > uid_max:
            result, data = server.uid('fetch', uid, '(RFC822)')  # fetch entire message
            msg = email.message_from_string(data[0][1])
            
            uid_max = uid
        
            text = get_first_text_block(msg)
            print('New message :::::::::::::::::::::')
            print(text)

    server.logout()
    time.sleep(5*60)"""
