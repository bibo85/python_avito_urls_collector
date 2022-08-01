import time
from urllib.request import Request, urlopen


def get_final_url(url: str):
    """
    Получаем конечный url после всех редиректов при переходе по ссылке
    :param url: ссылка с редиректом
    :return: final_url: str - конечный адрес после всех редиректов
    """
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'})
    number_of_attempts = 0
    while number_of_attempts < 3:
        try:
            webpage = urlopen(req, timeout=30)
            final_url = webpage.geturl()
            return final_url
        except Exception as exc:
            print('Не удалось перейти по ссылке:', url)
            print('Ошибка: ', exc)
            print('Пробуем еще раз')
            number_of_attempts += 1
            time.sleep(5)
    print('ВНИМАНИЕ! Финальный url не получен')
    return False
