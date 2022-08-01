import time
import requests
import gspread

from cookies import cookies
import engine
import settings

# устанавливаем основные настройки для работы парсера
print('Обращаемся к Гугл таблице')
google_account = gspread.service_account(filename=settings.google_json)  # настройка для подключения к гугл таблицам
source = google_account.open_by_url(settings.source_sheet_url)  # открываем таблицу с url
source_worksheet = source.worksheet(settings.source_name_worksheet)  # открываем лист с списком url
result_table = google_account.open_by_url(settings.result_sheet_url)  # открываем таблицу с результатами
result_worksheet = source.worksheet(settings.result_name_worksheet)  # открываем лист с результатами
col = settings.source_col  # колонка, из которой получаем url
current_row = settings.source_start_row  # текущая строка, с которой начнется сбор url
current_result_col = settings.result_start_col  # текущая строка для записи результатов

url = 'https://www.avito.ru/2396928366'

# Получаем конечный url после всех редиректов
final_url = engine.get_final_url(url)

# заменяем www в адресе на m, переводя ссылку на мобильную версию сайта
final_url = final_url.replace('www', 'm')
print(final_url)
time.sleep(5)
