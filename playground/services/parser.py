from html.parser import HTMLParser
import re
from urllib.request import urlopen
from urllib.error import HTTPError


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_header = False
        self.in_body = False
        self.in_p = False
        self.text = []
        self.error = False
        self.end = False

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
        if self.in_body and not self.in_header and self.in_p and not self.end:
            if ('а' <= data <= 'я' or 'А' <= data <= 'Я' or re.search("[,.?!-;:\"'ЇїЄє ]*", data)):
                if re.match("^©", data.strip()):
                    self.end = True
                else:
                    self.text.append(data.strip())

    def get_text(self):
        return " ".join(self.text)

    def get_error(self):
        return self.error


def prepare_data(url):
    parser = MyHTMLParser()
    try:
        response = urlopen(url)
        html_bytes = response.read()
        html = html_bytes.decode('windows-1251')
        parser.feed(html)
    except HTTPError:
        parser.error = True

    return parser


# class Parser():
#     def __init__(self):
#         self.error = False
#         self.end = False
#         self.text = []
        
#     def get_text(self):
#         return " ".join(self.text)
#     def get_error(self):
#         return self.error


# def prepare_data(url):
#     parser = Parser()
#     try:
#         response = urlopen(url)
#     except HTTPError:
#         parser.error = True
#     soup = BeautifulSoup(response, 'html.parser')

#     # Find the <body> tag
#     body_tag = soup.find('body')

#     # Find the <header> tag with the specific class
#     header_tag = body_tag.find('header')

#     # Find all subsequent <p> tags after the <header> tag
#     text_list = []
#     current_tag = header_tag.find_next_sibling()
#     while current_tag and current_tag.name == 'p' and not parser.end:
#         if re.match("^©", current_tag.get_text(strip=True)):
#             parser.end = True
#         else:
#             text_list.append(current_tag.get_text(strip=True))
#             current_tag = current_tag.find_next_sibling()

#     parser.text = text_list
#     return parser