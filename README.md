# Сборщик ссылок на профили с товаров на Avito

![Static Badge](https://img.shields.io/badge/python-3.10.4-blue)
![Static Badge](https://img.shields.io/badge/gspread-5.4.0-green)
![Static Badge](https://img.shields.io/badge/selenium-4.2.0-orange)
![Static Badge](https://img.shields.io/badge/beautifulsoup4-4.11.1-yellow)
![Static Badge](https://img.shields.io/badge/requests-2.28.1-cyan)
![Static Badge](https://img.shields.io/badge/termcolor-2.0.1-violet)

## Описание проекта
Скрипт позволяет получить ссылку на профиль пользователя, который выложил товар.

Как работает:
- Скрипт получает url адрес на товар из Google таблицы
- Ссылка из десктопной версии преобразуются в ссылку на мобильную версию
- Авторизация в личном кабинете по установленным файлам cookie
- Переход по подготовленной ссылке и получение ссылки на профиль пользователя
- Занесение полученной ссылки на профиль обратно в подготовленную Google таблицу
- Процесс повторяется, но уже со следующей строчкой, пока не будет достигнуто "Стоп" слово 

## Документация
1. Все зависимости описаны в файле __requirements.txt__
2. Инструкция по получению ключа авторизации в Google таблицах находится в файле __instruction.txt__
3. Необходимо заполнить файл cookie для авторизации.
   - авторизуемся на сайте Avito
   - копируем список с cookies из браузера
   - заносим информацию в файл ___cookies.py__
   - убираем нижнее подчеркивание в начале названия файла
```
# Пример:
# [
#     {
#         "name": "_dc_gtm_UA-2546784-1",
#         "value": "1",
#         "domain": ".avito.ru",
#         "hostOnly": False,
#         "path": "/",
#         "secure": False,
#         "httpOnly": False,
#         "sameSite": "no_restriction",
#         "session": False,
#         "firstPartyDomain": "",
#         "partitionKey": None,
#         "expirationDate": 1659344200,
#         "storeId": "firefox-default",
#         "id": 1
#     },
#     ...
# ]
cookies = []
```
4. Заполняем файл с настройками ___settings.py__
```
google_json = ''  # файл json для доступа к таблицам, полученный по инструкции в файле instruction.txt
source_sheet_url = ''  # адрес таблицы источника
source_name_worksheet = ''  # имя листа таблицы источника
source_col = ''  # колонка, из которой брать url (A, B, C...)
source_start__row = 2  # начальная строка, с которой берем url (1, 2, 3...)
source_end_text = 'Стоп'  # слово, по которому определяется конец списка url
result_sheet_url = ''  # адрес конечной таблицы
result_name_worksheet = ''  # имя листа конечной таблицы
current_result_row = 1  # строка, начиная с которой будет заполняться таблица (1, 2, 3...)
```
После заполнения убираем нижнее подчеркивание в начале файла.

5. Обязательно!!!
- предоставляем доступ на редактирование в рабочие таблицы для почты сервисного аккаунта гугла
Пример такой почты: parser@parser377917.iam.gserviceaccount.com
