import re

def validate(url):
    return re.match("^https://", url)
