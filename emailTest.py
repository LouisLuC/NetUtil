from imaplib import IMAP4
from email.parser import BytesParser
from email.policy import default
from config import CONFIG as cfg



password = cfg["password"]
server = cfg["email_host"] 
user = cfg["user"] 

im = IMAP4(server)
im.login(user, password)
im.select("INBOX")
status, uids = im.search(None, '(SUBJECT "P00533-P01137" SUBJECT "finished" FROM "yangzhanglab")')
status_1, uids_1 = im.search(None, '(SUBJECT "P00533-P01137")')
im.close()

status, msg = im.fetch(b'29', '(RFC822)')

msg = msg[0][1]
msg = msg.decode('utf8')




# TODO test if only term search