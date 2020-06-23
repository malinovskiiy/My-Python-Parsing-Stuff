import requests
from bs4 import BeautifulSoup
import csv
import os
from tkinter import *

root = Tk()

root.geometry('400x500')
root.title('Парсер новых авто сайта auto.ria.com')


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 Mobile Safari/537.36',
    'accept': '*/*'
}

HOST = 'https://auto.ria.com'
FILE = 'cars.csv'



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition_area')

    cars = []

    for item in items:

        uah_price = item.find('span', class_='grey size13')
        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = 'Price not found'
        cars.append({
            'title': item.find('div', class_='proposition_title')
            .find('h3', class_='proposition_name')
            .get_text(strip=True),
            'link': HOST + item.find('div', class_='proposition_title')
            .find('a').get('href'),
            'usd_price': item.find('span', class_='green').get_text(strip=True),
            'uah_price': uah_price,
            'city': item.find('svg', class_='svg-i16_pin').find_next('strong').get_text()
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена в $', 'Цена в грн', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['uah_price'], item['city']])


def parse():
    URL = url_entry.get().strip()
    html = get_html(URL)

    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            logger_text['text'] = 'Парсинг страницы {page} из {pages_count}...'
            html = get_html(URL, params={'page': page})
            get_content(html.text)
            cars.extend(get_content(html.text))

        save_file(cars, FILE)
        logger_text['text'] = f'Получено {len(cars)} автомобилей'
        os.startfile(FILE)
        # cars = get_content(html.text)
    else:
        print('Error')


title = Label(text='Введите url:', width=20, font='Arial 20')


url_entry = Entry(width=50)
parse_button = Button(width=43, text='Начать парсинг', command=parse)
logger_text = Label(width=50)

title.place(x=50, y=50)
url_entry.place(x=50, y=150)
parse_button.place(x=50, y=200)
logger_text.place(x=50, y=250)


root.mainloop()
