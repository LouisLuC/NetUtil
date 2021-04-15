import requests as rq
import time
import re

class WebListener:
    """
    The web listener listen to specific url, waiting for
    specific signal appear.
    """
    def listen(self, url, pattern, time_interval=300, time_out=1800, return_match=True):
        while True:
            rp = rq.get(url)
            if rp.ok: 
                match = re.search(pattern, rp.text)
                if match:
                    if return_match: return match 
                    else: return True
            time.sleep(time_interval)
