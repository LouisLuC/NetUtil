import imaplib as im
import email as em
import config as cfg

class EmailListener(im.IMAP4):
    def __init__(self, email_host, email_user, email_password, mail_box = "INBOX"):
        self.email_user     = email_user
        self.email_password = email_password
        self.email_host = email_host
        # creat pop3 linkage
        super().__init__(email_host)
        self.login(email_user, email_password)
        self.select(mail_box)

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
        
    def quit(self):
        self.close()
        bye = self.logout()
        return bye


if __name__ == "__main__":
    email = EmailListener(cfg.email_host, cfg.user, cfg.password)
    email.search(None, "SUBJECT", "Threpp")
    print(email.quit())
