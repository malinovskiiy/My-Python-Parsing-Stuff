import requests
from bs4 import BeautifulSoup
import csv
import time

PATH = 'file.csv'
URL = 'https://ru.investing.com/crypto/currencies'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 YaBrowser/20.6.0.905 Yowser/2.5 Safari/537.36 ',
    'accept': '*/*'
}


def get_html(url):
    r = requests.get(url, headers=HEADERS, params=None)
    return r.text


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table').find_all('tr')

    for tr in trs:
        time.sleep(1)
        try:
            name = tr.find('td', class_='cryptoName').find('a').get_text()
        except AttributeError:
            name = ''
        print(name)


def save_file(path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name', 'symbol', 'price'])


def main():
    html = get_html(URL)
    get_content(html)


main()
