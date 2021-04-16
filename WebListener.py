from os import system
import requests as rq
import time
import re

class WebListener:
    """
    The web listener listen to specific url, waiting for
    specific signal appear.
    """

    def listen(self, url, pattern, time_interval=300, time_out=1800, return_match=True):
        """
        listen to specific url, return when the pattern occur in the context of the web page

        :param url: url
        :param pattern: regular expression    
        :param time_interval: time interval of request the url 
        :param time_out: time_out
        :return_match: if True, return the match of regular expression 
        :return: True/ match of regular expression
        """
        while True:
            rp = rq.get(url)
            if rp.ok: 
                match = re.search(pattern, rp.text)
                if match:
                    if return_match: return match 
                    else: return True
            time.sleep(time_interval)


    def pull(self, url, location=None, rename=None, sh_cmd = "wget"):
        """
        """
        cmd = sh_cmd  
        if location:
            cmd += " -P " + location
        if rename:
            cmd += " -O " + rename
        cmd += url
        system(cmd)

