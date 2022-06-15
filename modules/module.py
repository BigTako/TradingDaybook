import sys, os
import time, datetime
import requests
from bs4 import BeautifulSoup

URL = 'https://ru.investing.com/economic-calendar/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
from datetime import datetime, timedelta

h_before = int(datetime.now().strftime('%H')) - 1
h_after = int(datetime.now().strftime('%H')) + 1
m = int(datetime.now().strftime('%M'))
time_before = str(timedelta(hours=h_before, minutes=m))
time_after = str(timedelta(hours=h_after, minutes=m))

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('tr', class_='js-event-item')
    news = []
    power = []
    for item in items:
        news.append([item.find('td', class_='left flagCur noWrap').get_text(strip=True),
                    item.find('td', class_='first left time js-time').get_text(strip=True),
                    item.find('td', class_='left textNum sentiment noWrap').get('title')
                        ])
    return news


def parse():
    global news
    html = get_html(URL)
    if html.status_code == 200:
        x = get_content(html.text)
        items = []
        for el in x:
            if el[2] == 'Умеренная волатильность' or el[2] == 'Высокая волатильность':
                if el[1] >= str(time_before) and el[1] <= str(time_after):
                    items.append(el[0])
        news = list(set(items))
        return news
    else:
        print("Error")







