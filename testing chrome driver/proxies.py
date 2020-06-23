import requests
from bs4 import BeautifulSoup
from random import choice


def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, headers=useragent, proxies=proxy)

