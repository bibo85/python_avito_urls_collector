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

# запускаем в работу парсер
while True:
    # получаем url
    print('Получаем url')
    url = engine.get_url_from_sheets(source_worksheet, col, current_row)

    # останавливаем парсер, если url больше нет
    if url == settings.source_end_text:
        break

    # берем следующую строку, если url пустой
    if not url:
        current_row += 1
        continue

    # Получаем конечный url после всех редиректов
    final_url = engine.get_final_url(url)

    # берем следующую строку, если не удалось получить финальный url
    if not final_url:
        current_row += 1
        continue

    # заменяем www в адресе на m, переводя ссылку на мобильную версию сайта и спим
    print('Меняем ссылку на мобильную версию и спим')
    final_url = final_url.replace('www', 'm')
    time.sleep(5)

    # получаем данные с сайта по финальному url
    print(f'Получаем данные по url: {final_url}')

    # получаем текст страницы
    response_text = engine.get_page_text(final_url)

    # получаем ссылку на профиль
    if not response_text:  # если ничего не вернулось, пробуем следующую строку
        current_row += 1
        continue

    # profile_url = engine.

    # добавляем ссылку в раблицу с результатами


    # спим и берем следующую строку
    print('Берем следующую строку и спим')
    time.sleep(10)
    current_row += 1
print('Скрипт завершил работу')
