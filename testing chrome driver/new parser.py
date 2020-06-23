import csv
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from random import choice

URL = 'https://www.avito.ru/barnaul/avtomobili?radius=200'
HOST = 'https://www.avito.ru'

driver = webdriver.Chrome('chromedriver.exe')

PATH = 'cars.csv'




HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 YaBrowser/20.6.0.905 Yowser/2.5 Safari/537.36 ',
    'access': '*/*'
}


def get_html(url, headers=None, params=None, proxy=None):
    r = requests.get(url, headers=headers, params=params, proxies=proxy)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = soup.find_all('span', class_='pagination-item-1WyVp')
    if int(pagination[-2].text) > 5:
        return 5
    else:
        return int(pagination[-2].text)


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')

    links = []

    items = soup.find_all('div', class_='snippet-horizontal')

    for item in items:
        links.append(HOST + item.find('a', class_='snippet-link').get('href'))

    return links


def get_page_data(html):
    driver.get(html)
    try:
        name = driver.find_element_by_class_name('title-info-title-text')
    except:
        name = ''
    driver.find_element_by_class_name('item-phone-button-sub-text').click()
    driver.implicitly_wait(10)
    # ActionChains(driver).move_to_element(button).click(button).perform()
    try:
        src = driver.find_element_by_xpath('/html/body/div[11]/div/div/div/div/div[1]/img').get_attribute('src')
    except:
        src = ''
    data = {
        'name': name,
        'src': src
    }

    return data


def get_proxy(url):
    html = get_html(url)

    proxies = html.text.split('\n')

    return proxies


def save_file(data):
    with open(PATH, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([data['name']])

        print(data['name'] + 'parsed')


def main():
    proxies = get_proxy('https://awmproxy.com/freeproxy_0c70317b2abaa65.txt')
    html = get_html(URL, HEADERS, proxy='http://' + choice(proxies))
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг ссылок со страницы {page} из {pages_count}...')
            html = get_html(URL, params={'p': page})
            cars.extend(get_content(html.text))
        for item in cars:
            save_file(get_page_data(item))

    else:
        print(html.status_code)
        print(html.headers)


if __name__ == '__main__':
    main()





