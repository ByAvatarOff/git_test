import requests
from bs4 import BeautifulSoup


URL = 'https://www.sunny-time.ru/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0', 'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='page-link')
    return int(pagination[-2].get_text())


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item-tour-pay-list')

    work = []

    for item in items:
        work.append({
            'City': str(item.find('div', class_='item-tour-title-block').get_text().replace('\n', ' ')),
            'Price': float(item.find('div', class_='price').get_text().replace('$', '')),
            'Count-people': item.find('div', class_='count-people').get_text(strip=True).replace('\n' + ' ' * 31, '')
        })
    return work


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = get_pages_count(html.text)
        work = []
        pages_count = 100
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            work.extend(get_content(html.text))
        pages_list = []
        for pag in range(1, pages_count*15 - 13):
            if 'Кипр' in work[pag].get('City') and 595 > work[pag].get('Price') > 550:
                pages_list.append(pag // 15 + 1)
        print(pages_list)
    else:
        print('Error')
        print('Hello')


parse()
