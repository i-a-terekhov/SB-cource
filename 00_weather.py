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


import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import cv2
import numpy as np
import json  # для сохранения словаря в файл weather_dict.py


class WeatherScraper:
    def __init__(self, url):
        self.url = url
        self.weather_row_data = {}
        self.new_weather_dict = {}

    def _fetch_data(self):
        """Через функции self._extract* переносим сырые данные в self.weather_row_data"""
        response = requests.get(self.url)
        if response.status_code == 200:
            text_of_response = response.text
            html_doc = BeautifulSoup(text_of_response, features='html.parser')

            self._extract_dates(html_doc)
            self._extract_times(html_doc)
            self._extract_contents(html_doc)
            self._extract_weather(html_doc)

    def _tags_to_list(self, tags):
        """Найденный парсингом текст помещаем в список"""
        list_of_text = []
        for tag in tags:
            received_text = tag.get_text(strip=True)
            if received_text != '':
                list_of_text.append(received_text)
            else:
                list_of_text.append(tag.get('title'))
        return list_of_text

    def _regular_filter(self, date_list):
        """Найденный текст с разноформатными датами переводим в унифицированный лист"""
        formatted_dates = []
        for date_str in date_list:
            date_of_month = re.search(r'\d+', date_str).group()
            month = re.search(r'(?!\s)\w+$', date_str).group()
            day_of_week = re.search(r'[а-я]+(?=,\s\d)|[а-я]+(?=\d+)', date_str).group()
            formatted_date_str = date_of_month + ' ' + month + ', ' + day_of_week
            formatted_dates.append(formatted_date_str)
        return formatted_dates

    def _extract_dates(self, html_doc):
        raw_days_dates = []

        tags_of_stand_days_dates = html_doc.find('div', {'class': 'pgd-short-cards pgd-short-cards_3-cards'}
                                                 ).find_all('span', {'class': 'pgd-short-card__date-title'})
        raw_days_dates.extend(self._tags_to_list(tags=tags_of_stand_days_dates))
        tags_of_extra_days_dates = html_doc.find('section', {'class': 'content-section-longrange_forecast'}
                                                 ).find_all('td', {'class': 'elements__section-day'})
        raw_days_dates.extend(self._tags_to_list(tags=tags_of_extra_days_dates))

        f_raw_days_dates = self._regular_filter(date_list=raw_days_dates)
        all_days_dates = []
        all_days_weekdays = []
        for date in f_raw_days_dates:
            date, weekday = date.split(', ')
            all_days_dates.extend([date, date, date, date])
            all_days_weekdays.extend([weekday, weekday, weekday, weekday])

        self.weather_row_data['dates'] = all_days_dates
        self.weather_row_data['weekdays'] = all_days_weekdays

    def _extract_times(self, html_doc):
        all_days_times = []

        tags_of_stand_days_times = html_doc.find_all('span', {'class': 'pgd-short-card__content-day-period'})
        all_days_times.extend(self._tags_to_list(tags=tags_of_stand_days_times))
        tags_of_extra_days_times = html_doc.find('table', {'data-weather-cards-count': '10forecast'}
                                                 ).find_all('td', {'class': 'elements__section-daytime'})
        for tags in tags_of_extra_days_times:
            tags_of_one_extra_day_times = tags.find_all('div', {'class': 'elements__section__item'})
            all_days_times.extend(self._tags_to_list(tags=tags_of_one_extra_day_times))

        self.weather_row_data['times'] = all_days_times

    def _extract_contents(self, html_doc):
        all_days_contents = []

        tags_of_stand_days_content = html_doc.find('div', {'class': 'pgd-short-cards pgd-short-cards_3-cards'}
                                                   ).find_all('span', {'class': 'pgd-short-card__content-weather'})
        all_days_contents.extend(self._tags_to_list(tags=tags_of_stand_days_content))
        tags_of_extra_days_contents = html_doc.find('section', {'class': 'content-section-longrange_forecast'}
                                                    ).find_all('td', {'class': 'elements__section-temperature'})
        for tags in tags_of_extra_days_contents:
            tags_of_one_extra_day_content = tags.find_all('div', {'class': 'elements__section__view-short'})
            all_days_contents.extend(self._tags_to_list(tags=tags_of_one_extra_day_content))

        self.weather_row_data['contents'] = all_days_contents

    def _extract_weather(self, html_doc):
        all_days_weather = []

        tags_of_stand_days_weather = html_doc.find('div', {'class': 'pgd-short-cards pgd-short-cards_3-cards'}
                                                   ).find_all('i', {'class': 'icon-weather'})
        all_days_weather.extend(self._tags_to_list(tags=tags_of_stand_days_weather))
        tags_of_extra_days_weather = html_doc.find('section', {'class': 'content-section-longrange_forecast'}
                                                   ).find_all('td', {'class': 'elements__section-weather'})
        for tags in tags_of_extra_days_weather:
            tags_of_one_extra_day_weather = tags.find_all('i', {'class': 'icon-weather'})
            all_days_weather.extend(self._tags_to_list(tags=tags_of_one_extra_day_weather))

        self.weather_row_data['weather'] = all_days_weather

    def _translate_weather_row_data(self, weather_row_data):
        #TODO Необходим один словарь, для всех переводов, сохраняемый в файле, т.к. заранее нельзя предсказать, какие
        # фразы будут использованы.
        pass

    def _translate_datas(self, d):
        month_translate = {
            'янв': ' of January',
            'фев': ' of February',
            'мар': ' of March',
            'апр': ' of April',
            'мая': ' of May',
            'июн': ' of June',
            'июл': ' of July',
            'авг': ' of August',
            'сен': ' of September',
            'окт': ' of October',
            'ноя': ' of November',
            'дек': ' of December',

        }
        day, month = d.split()
        month = month_translate[month[:3]]
        return day + month

    def _translate_weekday(self, wd):
        weekday_translate = {
            'понедельник': 'Monday',
            'вторник': 'Tuesday',
            'среда': 'Wednesday',
            'четверг': 'Thursday',
            'пятница': 'Friday',
            'суббота': 'Saturday',
            'воскресенье': 'Sunday',
        }
        return weekday_translate[wd]

    def _translate_times(self, t):
        time_translate = {
            'утро': 'morning',
            'день': 'nune',
            'вечер': 'evening',
            'ночь': 'night',

        }
        return time_translate[t]

    def _translate_weather(self, w):
        weather_translate = {
            'Ясная погода, без осадков': 'Clear weather, no precipitation',
            'Небольшая облачность, без осадков': 'Partly cloudy, no precipitation',
            'Переменная облачность, без осадков': 'Variable cloudiness, no precipitation',
            'Пасмурно, без осадков': 'Overcast, no precipitation',
            'Пасмурно, небольшие дожди': 'Overcast, light rain',
            'Облачно, без осадков': 'Cloudy, no precipitation',
            'Переменная облачность, небольшие дожди': 'Variable cloudiness, light rain',
        }
        w = weather_translate.get(w)
        return w

    def _create_weather_dict(self):
        self._translate_weather_row_data(self.weather_row_data)

        dates = self.weather_row_data['dates']
        weekdays = self.weather_row_data['weekdays']
        times = self.weather_row_data['times']
        contents = self.weather_row_data['contents']
        weather = self.weather_row_data['weather']

        for d, wd, t, c, w in zip(dates, weekdays, times, contents, weather):
            d = self._translate_datas(d)
            wd = self._translate_weekday(wd)
            t = self._translate_times(t)
            w = self._translate_weather(w)

            # print(f'{d:>13}, {wd:12} - {t:6} {c} - {w}')
            entry = {
                'weekday': wd,
                'content': c,
                'weather': w
            }
            if d not in self.new_weather_dict:
                self.new_weather_dict[d] = {}

            self.new_weather_dict[d][t] = entry

        # pprint(self.new_weather_dict)

    def run(self):
        self._fetch_data()
        self._create_weather_dict()
        output_file = 'weather_dict.json'
        #TODO Пока функция перезаписывает json заново. В дальнейшем необходимо сделать выгрузку из json,
        # обновление словаря новыми данными, и затем запись в json:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(self.new_weather_dict, file, ensure_ascii=False, indent=4)

    def return_the_final_dict(self):
        return self.new_weather_dict


class ImageMaker:

    def __init__(self):
        self.form = 'python_snippets/external_data/probe.jpg'
        # self.form = 'python_snippets/external_data/girl.jpg'  # Временная картинка для отработки масштабирования
        # self.form = 'python_snippets/external_data/photos/1skillbox.png'  # Картинка много меньше max window sizes

    def view_image(self, image, name_of_window):
        max_window_width = 800
        max_window_height = 600

        window_height, window_width = max_window_height, max_window_width

        image_height, image_width = image.shape[:2]
        crop_factor_height = image_height / max_window_height
        crop_factor_width = image_width / max_window_width

        if 1 < crop_factor_width > crop_factor_height:
            window_height = int(image_height / crop_factor_width)
        elif 1 < crop_factor_height > crop_factor_width:
            window_width = int(image_width / crop_factor_height)
        else:
            window_width, window_height = image_width, image_height

        with open('weather_dict.json', 'r', encoding='utf-8') as file:
            weather_data = json.load(file)
        original_dict = weather_data
        print(original_dict['28 of September']['nune']['weather'])

        text = original_dict['28 of September']['nune']['weather']

        font = cv2.FONT_HERSHEY_DUPLEX
        font_color = (0, 255, 0)
        start_font_scale = 20
        start_font_thickness = start_font_scale // 2

        max_text_width = int(0.8 * image_width)
        (start_text_width, _), _ = cv2.getTextSize(text, font, start_font_scale, start_font_thickness)
        font_scale = int(start_font_scale * (max_text_width / start_text_width))
        if font_scale == 0:
            font_scale = 1
        font_thickness = int(font_scale // 2)

        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        position = (int((image_width - text_width) / 2), int((image_height + text_height) / 2))

        cv2.putText(image, text, position, font, font_scale, font_color, font_thickness)

        cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name_of_window, window_width, window_height)
        cv2.imshow(name_of_window, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run(self):
        image_cv2 = cv2.imread(self.form)
        self.view_image(image_cv2, 'Original version')


if __name__ == "__main__":
    url = 'https://pogoda.ngs.ru/?from=pogoda'
    # get_weather = WeatherScraper(url)
    # get_weather.run()
    # pprint(get_weather.return_the_final_dict())

    #TODO img.run() берет значения из словаря, формируемого и обновляемого в get_weather.run()
    img = ImageMaker()
    img.run()

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
