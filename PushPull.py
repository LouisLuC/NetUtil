import requests as rq
from os import system


def pull(url, location=None, rename=None, sh_cmd = "wget"):
    cmd = sh_cmd  
    if location:
        cmd += " -P " + location
    if rename:
        cmd += " -O " + rename
    cmd += url
    system(cmd)

