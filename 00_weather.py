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


def tags_to_list(tags):
    list = []
    for tag in tags:
        received_text = tag.get_text(strip=True)
        if received_text != '':
            list.append(received_text)
        else:
            list.append(tag.get('title'))
    return list


response = requests.get('https://pogoda.ngs.ru/?from=pogoda')

if response.status_code == 200:
    text_of_response = response.text
    html_doc = BeautifulSoup(text_of_response, features='html.parser')

    tags_of_stand_days_dates = html_doc.find('div', {'class': 'pgd-short-cards pgd-short-cards_3-cards'}
                                             ).find_all('span', {'class': 'pgd-short-card__date-title'})
    stand_days_dates = tags_to_list(tags_of_stand_days_dates)

    tags_of_extra_days_dates = html_doc.find('section', {'class': 'content-section-longrange_forecast'}
                                             ).find_all('td', {'class': 'elements__section-day'})
    extra_days_dates = tags_to_list(tags_of_extra_days_dates)

    tags_of_stand_days_times = html_doc.find_all('span', {'class': 'pgd-short-card__content-day-period'})
    stand_days_times = tags_to_list(tags_of_stand_days_times)

    tags_of_extra_days_times = html_doc.find_all('td', {'class': 'elements__section-daytime'})
    extra_days_times = []
    for tags in tags_of_extra_days_times:
        tags_of_one_extra_day_times = tags.find_all('div', {'class': 'elements__section__item'})
        extra_days_times.extend(tags_to_list(tags_of_one_extra_day_times))

    tags_of_stand_days_content = html_doc.find('div', {'class': 'pgd-short-cards pgd-short-cards_3-cards'}
                                               ).find_all('span', {'class': 'pgd-short-card__content-weather'})
    stand_days_contents = tags_to_list(tags_of_stand_days_content)

    tags_of_extra_days_contents = html_doc.find('section', {'class': 'content-section-longrange_forecast'}
                                                ).find_all('td', {'class': 'elements__section-temperature'})
    extra_days_contents = []
    for tags in tags_of_extra_days_contents:
        tags_of_one_extra_day_content = tags.find_all('div', {'class': 'elements__section__view-short'})
        extra_days_contents.extend(tags_to_list(tags_of_one_extra_day_content))

    tags_of_stand_days_weather = html_doc.find('div', {'class': 'pgd-short-cards pgd-short-cards_3-cards'}
                                               ).find_all('i', {'class': 'icon-weather'})
    stand_days_weather = tags_to_list(tags_of_stand_days_weather)

    tags_of_extra_days_weather = html_doc.find('section', {'class': 'content-section-longrange_forecast'}
                                               ).find_all('td', {'class': 'elements__section-weather'})
    extra_days_weather = []
    for tags in tags_of_extra_days_weather:
        tags_of_one_extra_day_weather = tags.find_all('i', {'class': 'icon-weather'})
        extra_days_weather.extend(tags_to_list(tags_of_one_extra_day_weather))

    # TODO добавить форматирование дат под один стандарт:
    all_days_dates = []
    for date in stand_days_dates:
        all_days_dates.extend([date, date, date, date])
    for date in extra_days_dates:
        all_days_dates.extend([date, date, date, date])

    all_days_times = []
    all_days_times.extend(stand_days_times)
    all_days_times.extend(extra_days_times)

    all_days_contents = []
    all_days_contents.extend(stand_days_contents)
    all_days_contents.extend(extra_days_contents)

    all_days_weather = []
    all_days_weather.extend(stand_days_weather)
    all_days_weather.extend(extra_days_weather)

    for d, t, c, i in zip(all_days_dates, all_days_times, all_days_contents, all_days_weather):
        print(f'{d:>30} - {t:7} {c} - {i}')

    print(all_days_dates)
