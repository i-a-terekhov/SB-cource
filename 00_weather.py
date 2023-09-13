# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погода
# Из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database


# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from pprint import pprint

response = requests.get('https://pogoda.ngs.ru/?from=pogoda')

if response.status_code == 200:
    text_of_response = response.text
    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(text_of_response)
    # print("HTML-код сохранен в файл 'output.html'")

    html_doc = BeautifulSoup(text_of_response, features='html.parser')

    wrong_tag = html_doc.find('table', {'class': 'pgd-detailed-cards elements pgd-hidden'})
    wrong_tag.decompose()
    print('Удалены лишние теги')
    print('-' * 100)

    #TODO list_of_all_dates требует разделения на две переменных: для стандартных и экстра дней
    list_of_all_dates = html_doc.find_all('span', {'class': 'pgd-short-card__date-title'})
    print('list_of_all_dates:')
    pprint(list_of_all_dates)
    print('-' * 100)

    periods_in_stand_dates = html_doc.find_all('span', {'class': 'pgd-short-card__content-day-period'})
    print('periods_in_stand_dates:')
    pprint(periods_in_stand_dates)
    print('-' * 100)

    periods_in_extra_dates = html_doc.find_all('td', {'class': 'elements__section-daytime'})
    extra_days_periods = []
    for extra_day in periods_in_extra_dates:
        period_of_one_extra_day = extra_day.find_all('div', {'class': 'elements__section__item'})
        extra_days_periods.extend(period_of_one_extra_day)
    print('periods_in_extra_dates:')
    pprint(extra_days_periods)
    print('-' * 100)

    list_of_content_stand_days = html_doc.find('div', {'class': 'pgd-short-cards pgd-short-cards_3-cards'})
    content = list_of_content_stand_days.find_all('span', {'class': 'pgd-short-card__content-weather'})
    print('list_of_content_stand_days:')
    pprint(content)
    print('-' * 100)

    list_of_extra_content = html_doc.find_all('td', {'class': 'elements__section-temperature'})
    extra_term = []
    for extra_temp in list_of_extra_content:
        temp = extra_temp.find_all('div', {'class': 'elements__section__item'})
        #TODO добавить отображение только содержания тегов в предыдущие листы по этому примеру:
        for element in temp:
            text_content = element.get_text(strip=True)  # strip=True удаляет лишние пробелы и символы новой строки
            extra_term.append(text_content)
    print('list_of_extra_content:')
    pprint(extra_term)

    # for d, p, c in zip(list_of_all_dates, periods_in_stand_dates, list_of_content_stand_days):
    #     print(d.text, p.text, c.text)


