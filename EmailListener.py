import imaplib as im
import email as em
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.policy import default

class EmailListener(im.IMAP4):
    def __init__(self, email_host, email_user, email_password):
        self.email_user     = email_user
        self.email_password = email_password
        self.email_host = email_host
        # creat pop3 linkage
        super().__init__(email_host)


    def listen(self, search_term, pattern, return_match = False, time_interval=300, time_out=1800):
        import re
        import time
        while True:
            status, uids = self.search(None, search_term)
            if status == "OK" and len(uids) > 0:
                uid = uids[0]
                status, msg = self.fetch(uid, '(RFC822)')
                if status == "OK":
                    match = re.search(pattern, msg[0][1].decode("utf9"))
                    if match:
                        if return_match:
                            return match
                        else:
                            return True
            time.sleep(time_interval)       


