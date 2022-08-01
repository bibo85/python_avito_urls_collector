import time
import gspread

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
current_result_row = settings.result_start_row  # текущая строка для записи результатов

# запускаем в работу парсер
while True:
    try:
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
            time.sleep(10)
            continue

        # заменяем www в адресе на m, переводя ссылку на мобильную версию сайта и спим
        print('Меняем ссылку на мобильную версию и спим')
        final_url = final_url.replace('www', 'm')
        time.sleep(5)

        # получаем данные с сайта по финальному url
        print(f'Получаем данные по url: {final_url}')

        # получаем текст страницы
        html = engine.get_page_text(final_url)

        # получаем ссылку на профиль
        if not html:  # если ничего не вернулось, пробуем следующую строку
            print('Не удалось получить html страницы. Пробуем следующую ссылку')
            current_row += 1
            continue

        link_to_profile = engine.html_parser(html)
        if not link_to_profile:
            print('ОШИБКА! Не удалось получить ссылку на профиль')
            current_row += 1
            time.sleep(10)
            continue

        # добавляем ссылку на профиль в таблицу с результатами
        print(f'Добавляем ссылку на профиль в таблицу с результатами')
        result_worksheet.update_cell(current_result_row, 1, link_to_profile)
    except Exception as exc:
        print('Ошибка!')
        print(exc)
    # спим и берем следующую строку
    print('Берем следующую строку и спим')
    time.sleep(10)
    current_result_row += 1
    current_row += 1
print('Скрипт завершил работу')
