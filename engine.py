import time
import requests
from urllib.request import Request, urlopen
from cookies import cookies


def get_final_url(url: str):
    """
    Получаем конечный url после всех редиректов при переходе по ссылке
    :param url: ссылка с редиректом
    :return: final_url: str - конечный адрес после всех редиректов
    """
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'})
    connection_attempts = 0
    while connection_attempts < 5:
        try:
            webpage = urlopen(req, timeout=30)
            final_url = webpage.geturl()
            print('Финальный url получен')
            return final_url
        except Exception as exc:
            print('Не удалось перейти по ссылке:', url)
            print('Ошибка: ', exc)
            print('Пробуем еще раз')
            connection_attempts += 1
            time.sleep(5)
    print('ВНИМАНИЕ! Финальный url не получен')
    return False


def get_url_from_sheets(source_worksheet, col, current_row):
    """
    Получаем url из рабочей таблицы, по которому будем собирать данные.
    :param source_worksheet: текущий рабочий лист, к которому обращаемся
    :param col: колонка, из которой берем данные
    :param current_row: текущая строка, из которой берем данные
    :return: url: str - полученный url из таблицы
    """
    sec = 0  # сколько секунд спим перед попытками
    connection_attempts = 0  # счетчик попыток
    url = None
    # если попыток меньше 5, то снова пробуем получить url, каждый раз спим дольше
    while connection_attempts < 5:
        time.sleep(sec)
        try:
            url = source_worksheet.acell(f'{col}{current_row}').value
            break
        except Exception as exc:
            print('Не удалось получить url')
            print(f'Ошибка {exc}')
            connection_attempts += 1
            sec += 2
    return url


def get_page_text(url):
    # создаем строку с cookies
    cookies_in_string = ''
    for cookie in cookies:
        cookies_in_string += f"{cookie['name']}={cookie['value']}; "

    # Делаем запрос в рамках одной сессии
    request = requests.Session()

    # Задаем заголовки:
    headers = {'authority': 'm.avito.ru',
               'pragma': 'no-cache',
               'cache-control': 'no-cache',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'sec-fetch-site': 'none',
               'sec-fetch-mode': 'navigate',
               'sec-fetch-user': '?1',
               'sec-fetch-dest': 'document',
               'accept-language': 'ru-RU,ru;q=0.9', }
    if cookies_in_string:  # Добавим куки, если есть внешние куки
        headers['cookie'] = cookies_in_string
    else:
        print('Необходимо задать куки в отдельном файле cookies.py')
        return False

    # Сохраняем заголовки в сессию
    request.headers.update(headers)

    # Переходим по ссылке
    sec = 0  # сколько секунд спим перед попытками
    connection_attempts = 0  # счетчик попыток
    response = None
    # если попыток меньше 5, то снова пробуем получить url, каждый раз спим дольше
    while connection_attempts < 5:
        time.sleep(sec)
        try:
            response = request.get(url, timeout=30)
            return response.text
        except Exception as exc:
            print('Не удалось получить текст страницы: ', url)
            print(f'Ошибка {exc}')
            print('Пробуем еще раз')
            connection_attempts += 1
            sec += 3
    return response
