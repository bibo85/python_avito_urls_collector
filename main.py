import time
import requests

from cookies import cookies
import engine

url = 'https://www.avito.ru/2396928366'

# Получаем конечный url после всех редиректов
final_url = engine.get_final_url(url)

# заменяем www в адресе на m, переводя ссылку на мобильную версию сайта
final_url = final_url.replace('www', 'm')
print(final_url)
time.sleep(5)
