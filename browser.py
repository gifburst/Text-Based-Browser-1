import sys
import os
import requests
import bs4
import colorama
from colorama import Fore, Back, Style


TERMINATE_STRING = "__"
ERROR_MESSAGE = "error"
DIR = sys.argv[1]
if not os.path.exists(DIR):
    os.mkdir(DIR)
os.stat(DIR)
TAGS = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"]
colorama.init()


def parse_query(query, stack_of_pages):
    try:
        if query == "exit":
            return TERMINATE_STRING
        elif query == "back":
            stack_of_pages[-2]
            return stack_of_pages.pop()
        else:
            if len(query) >= len(".com") and (query[-len(".com"):] == ".com" or
                                            query[-len(".org"):] == ".org"):
                url = query
                if len(url) < len("https://") or url[:len("https://")] != "https://":
                    url = "https://" + url
                text = ""
                if not os.path.exists(os.path.join(DIR, url[len("https://"): -len(".com")])):
                    html = requests.get(url).content
                    soup = bs4.BeautifulSoup(html, 'html.parser')
                    text = ''.join((Fore.BLUE + st.get_text() + Style.RESET_ALL if st.name == 'a' else st.get_text() for st in soup.find_all(TAGS)))
                    with open(os.path.join(DIR, url[len("https://"): -len(".com")]), "w") as f:
                        f.write(text)
                else:
                    with open(os.path.join(DIR, url[len("https://"): -len(".com")]), "r") as f:
                        text = f.read()
                return text
            f = open(os.path.join(DIR, query), 'r')
            text = f.read()
            return text
    except:
        return ERROR_MESSAGE



if __name__ == "__main__":
    stack_of_pages = list()
    while True:
        output = parse_query(input(), stack_of_pages)
        if output == TERMINATE_STRING:
            break
        else:
            print(output)
            if output != ERROR_MESSAGE:
                stack_of_pages.append(output)
