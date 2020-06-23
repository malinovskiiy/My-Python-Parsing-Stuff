import csv
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

URL = 'https://coinmarketcap.com/ru/all/views/all/'
HOST = 'https://coinmarketcap.com'


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 YaBrowser/20.6.0.905 Yowser/2.5 Safari/537.36 ',
    'access': '*/*'
}


PATH = 'data.csv'


def get_html(url, headers=None):
    r = requests.get(url, headers=headers)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')

    tds = soup.find_all('td', class_='cmc-table__cell--sort-by__name')

    links = []

    for td in tds:
        a = HOST + td.find('div').find('a').get('href')
        links.append(a)

    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1').text.strip()
    except:
        name = 'No name'

    try:
        price = soup.find('span', class_='cmc-details-panel-price__price').text.strip() + ' USD'
    except:
        price = 'No price'

    data = {
        'name': name,
        'price': price
    }

    return data


def save_file(data):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([data['name'], data['price']])

        print(data['name'], 'parsed')


def make_all(url):
    html = get_html(url, HEADERS)
    data = get_page_data(html)
    save_file(data)


def main():
    all_links = get_all_links(get_html(URL))

    with Pool(40) as p:
        p.map(make_all, all_links)


if __name__ == '__main__':
    main()
