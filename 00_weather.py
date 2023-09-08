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

# response = requests.get('https://yandex.com.ge/weather/batumi')
response = requests.get('https://pogoda.ngs.ru/?from=pogoda')

if response.status_code == 200:
    html_doc = BeautifulSoup(response.text, features='html.parser')

    list_of_date = html_doc.find_all('span', {'class': 'pgd-short-card__date-title'})
    list_of_period = html_doc.find_all('span', {'class': 'pgd-short-card__content-day-period'})

    temperature_pars = html_doc.find_all('td', {'class': 'elements__section-daytime'})
    # TODO на странице существуют неактивные в инспекторе строке, одна из них попадает в фильтр find_all
    temperature_sections = []
    for elem in temperature_pars:
        temperature = elem.find_all('div', {'class': 'elements__section__item'})
        temperature_sections.extend(temperature)

    list_of_content = html_doc.find_all('span', {'class': 'pgd-short-card__content-weather'})

# list_of_weather = html_doc.select('span') # TODO этот метод тоже надо изучить

    pprint(list_of_date)
    pprint(list_of_period)
    pprint(temperature_sections)
    pprint(list_of_content)

    for d, p, c in zip(list_of_date, list_of_period, list_of_content):
        print(d.text, p.text, c.text)

        #TODO Возможно, сайт воспринимает запросы как спам - это нужно проверить
        # да, это так

