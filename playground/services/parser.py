from html.parser import HTMLParser
#from urllib.request import urlopen
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_header = False
        self.in_body = False
        self.in_p = False
        self.in_p = False
        self.text = []
        self.error = False

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
        elif tag == "header":
            self.in_header = True
        elif self.in_body and tag == "p":
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False
        elif tag == "header":
            self.in_header = False
        elif self.in_body and tag == "p" and self.in_p:
            self.in_p = False

    def handle_data(self, data):
        if self.in_body and not self.in_header and self.in_p:
            if 'а' <= data <= 'я' or 'А' <= data <= 'Я' or re.search("[,.?!-;:\"' ]", data):
                self.text.append(data.strip())

    def get_text(self):
        return " ".join(self.text)

    def get_error(self):
        return self.error


def prepare_data(url):
    response = urlopen(url)
    html_bytes = response.read()
    html = html_bytes.decode('windows-1251')
    parser = MyHTMLParser()
    parser.feed(html)
    return parser
    """try:
        response = urlopen(url)
        html_bytes = response.read()
        html = html_bytes.decode('windows-1251')
        parser = MyHTMLParser()
        parser.feed(html)
        return parser.get_text()
    except HTTPError as err:
        parser.error = True"""
    