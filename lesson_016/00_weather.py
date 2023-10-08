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
import re
import cv2
import numpy as np
import json
from datetime import datetime, timedelta
from pprint import pprint
import os
from SQLDataUpdater import WeatherData


class WeatherScraper:
    def __init__(self):
        self.url = 'https://pogoda.ngs.ru/?from=pogoda'
        self.weather_row_data = {}
        self.new_weather_dict = {}

    def fetch_data(self):
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
        all_days_full_dates = []
        for date in f_raw_days_dates:
            date, weekday = date.split(', ')
            all_days_dates.extend([date, date, date, date])
            all_days_weekdays.extend([weekday, weekday, weekday, weekday])
            fd = str(str_en_date_to_date(self._translate_datas(date)))
            all_days_full_dates.extend([fd, fd, fd, fd])

        self.weather_row_data['dates'] = all_days_dates
        self.weather_row_data['weekdays'] = all_days_weekdays
        self.weather_row_data['full_dates'] = all_days_full_dates

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
            'Пасмурно, снег с дождем': 'Cloudy, snow and rain',
        }
        w = weather_translate.get(w, w)
        return w

    def _create_weather_dict(self):
        dates = self.weather_row_data['dates']
        weekdays = self.weather_row_data['weekdays']
        times = self.weather_row_data['times']
        contents = self.weather_row_data['contents']
        weather = self.weather_row_data['weather']
        full_dates = self.weather_row_data['full_dates']

        for d, wd, t, c, w, fd in zip(dates, weekdays, times, contents, weather, full_dates):
            d = self._translate_datas(d)
            wd = self._translate_weekday(wd)
            t = self._translate_times(t)
            w = self._translate_weather(w)

            # print(f'{d:>13}, {wd:12} - {t:6} {c} - {w}')
            entry = {
                'weekday': wd,
                'content': c,
                'weather': w,
                'full_date': fd,
            }
            if d not in self.new_weather_dict:
                self.new_weather_dict[d] = {}

            self.new_weather_dict[d][t] = entry

        # pprint(self.new_weather_dict)

    def return_the_final_dict(self, output=False):
        if len(self.weather_row_data) > 0:
            self._create_weather_dict()
            if output:
                pprint(self.new_weather_dict)
            return self.new_weather_dict
        else:
            raise Exception('Словарь текущей погоды не сформирован')


def str_en_date_to_date(date_str):
    today = datetime.now().date()
    parts = date_str.split(' of ')
    day = int(parts[0])
    month = datetime.strptime(parts[1], '%B').month
    return datetime(today.year, month, day).date()


def date_to_str_en_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d of %B")
    if formatted_date.startswith("0"):
        formatted_date = formatted_date[1:]
    return formatted_date


class JSONDatabaseUpdater:
    def __init__(self):
        self.database_name = r'C:\Users\Ivan\PyCharm\SkillBox\lesson_016\weather_dict.json'
        self.weather_data = None

    def refresh_database(self, new_weather_dict, make_copy=False):
        bd_full_path = self.database_name
        with open(bd_full_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)

        existing_data.update(new_weather_dict)

        if make_copy:
            directory, filename = os.path.split(bd_full_path)
            filename, extension = os.path.splitext(filename)
            new_filename = f'{filename}_copy{extension}'
            bd_full_path = os.path.join(directory, new_filename)
            print('Создана копия', bd_full_path, '\n')

        with open(bd_full_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    def update_old_type_database(self):
        with open(self.database_name, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)

        for date in existing_data:
            for time in existing_data[date]:
                # добавляем новый ключ:
                if 'full_date' not in existing_data[date][time].keys():
                    fd = str(str_en_date_to_date(date))
                    existing_data[date][time]['full_date'] = fd
                # удаляем некорректный ключ:
                if 'full_dates' in existing_data[date][time].keys():
                    del existing_data[date][time]['full_dates']

        with open(self.database_name, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    def _get_datas_from_bd(self):
        with open(self.database_name, 'r', encoding='utf-8') as file:
            self.weather_data = json.load(file)

    def return_data_for_selected_days(self, days=None):
        if not self.weather_data:
            self._get_datas_from_bd()

        data_for_selected_days = {}
        date_list = self.weather_data.keys()
        if days is None:
            today = datetime.now().date()
            max_weather_cards = 5
            selected_dates = 0
            for date_str in date_list:
                date = str_en_date_to_date(date_str)
                if date >= today:
                    selected_dates += 1
                    data_for_selected_days[date_str] = self.weather_data[date_str]
                if selected_dates >= max_weather_cards:
                    break
        else:
            for day in days:
                if day in date_list:
                    data_for_selected_days[day] = self.weather_data[day]
        # print(f'Доступен прогноз на следующие дни: {list(data_for_selected_days.keys())}')
        return data_for_selected_days

    def return_data_for_all_days(self):
        if not self.weather_data:
            self._get_datas_from_bd()
        return self.weather_data


def save_weather_data(weather_dict):
    for day, day_content in weather_dict.items():
        for time, time_content in day_content.items():
            weekday = time_content.get('weekday')
            content = time_content.get('content')
            weather = time_content.get('weather')
            full_date = time_content.get('full_date')
            # print(f'Взяли данные из словаря: {day:15}, {time:7}, {weekday:9}, {content:4}, {weather}, {full_date:8}')

            try:
                weather_data = WeatherData.get(day=day, time=time)
                # Если запись существует, обновляем ее
                weather_data.weekday = weekday
                weather_data.content = content
                weather_data.weather = weather
                weather_data.full_date = full_date
                weather_data.save()
            except WeatherData.DoesNotExist:
                # Если запись не найдена, создаем новую
                WeatherData.create(
                    day=day,
                    time=time,
                    weekday=weekday,
                    content=content,
                    weather=weather,
                    full_date=full_date
                )


class ImageMaker:

    def __init__(self):
        self.form = r'C:\Users\Ivan\PyCharm\SkillBox\lesson_016\python_snippets\external_data\probe.jpg'
        self.datas = {}

    def _get_window_sizes(self, image_height, image_width):
        max_window_width = 800
        max_window_height = 600

        window_height, window_width = max_window_height, max_window_width

        crop_factor_height = image_height / max_window_height
        crop_factor_width = image_width / max_window_width

        if 1 < crop_factor_width > crop_factor_height:
            window_height = int(image_height / crop_factor_width)
        elif 1 < crop_factor_height > crop_factor_width:
            window_width = int(image_width / crop_factor_height)
        else:
            window_width, window_height = image_width, image_height
        return window_height, window_width

    def _print_non_scale_text(self, image, text, position, scale):
        font = cv2.FONT_HERSHEY_DUPLEX
        font_color = (0, 255, 0)
        font_scale = scale
        font_thickness = 1
        cv2.putText(image, text, position, font, font_scale, font_color, font_thickness)

    def _print_scale_text(self, image, text_weather, image_height, image_width):
        font = cv2.FONT_HERSHEY_DUPLEX
        font_color = (0, 255, 0)
        start_font_scale = 20
        start_font_thickness = start_font_scale // 2
        max_text_width = int(0.8 * image_width)

        # Получение ширины текста при стартовых размере и толщине шрифта:
        (start_text_width, _), _ = cv2.getTextSize(text_weather, font, start_font_scale, start_font_thickness)
        font_scale = int(start_font_scale * (max_text_width / start_text_width))
        if font_scale == 0:
            font_scale = 1
        font_thickness = int(font_scale // 2)

        # Вычисление ширины и высоты текста при итоговых размере и толщине шрифта для определения начальной точки
        (text_width, text_height), _ = cv2.getTextSize(text_weather, font, font_scale, font_thickness)
        position = ((image_width - text_width) // 2, int((1.6 * image_height + text_height) // 2))
        cv2.putText(image, text_weather, position, font, font_scale, font_color, font_thickness)

    def _choose_an_icon(self, data):
        location = r'C:\Users\Ivan\PyCharm\SkillBox\lesson_016\python_snippets\external_data\weather_img'
        weather_icon = {
            'Clear weather, no precipitation': 'sun.jpg',
            'Partly cloudy, no precipitation': 'cloud.jpg',
            'Variable cloudiness, no precipitation': 'cloud.jpg',
            'Overcast, no precipitation': 'cloud.jpg',
            'Overcast, light rain': 'rain.jpg',
            'Cloudy, no precipitation': 'cloud.jpg',
            'Variable cloudiness, light rain': 'rain.jpg',
            'Cloudy, snow and rain': 'snow.jpg',
        }
        icon_path = location + '\\' + weather_icon[self.datas[data]['nune']['weather']]
        return icon_path

    def _gradient_maker(self, data, image_height, image_width):
        weather_colors = {
            'Clear weather, no precipitation': [(255, 255, 0), (255, 255, 255)],  # Желтый к белому
            'Partly cloudy, no precipitation': [(0, 0, 128), (255, 255, 255)],  # Синий к белому
            'Variable cloudiness, no precipitation': [(135, 206, 235), (255, 255, 255)],  # Голубой к белому
            'Overcast, no precipitation': [(169, 169, 169), (255, 255, 255)],  # Серый к белому
            'Overcast, light rain': [(169, 169, 169), (0, 0, 255)],  # Серый к синему
            'Cloudy, no precipitation': [(169, 169, 169), (255, 255, 255)],  # Серый к белому
            'Variable cloudiness, light rain': [(135, 206, 235), (0, 0, 255)],  # Голубой к синему
            'Cloudy, snow and rain': [(169, 169, 169), (255, 255, 255)],  # Серый к белому
        }

        weather = self.datas[data]['nune']['weather']
        start_color = weather_colors[weather][0]
        end_color = weather_colors[weather][1]

        # создаем холст для градиента
        # Возможно улучить: проверяем, есть ли подходящий сохраненный градиент. Если нет, создаем и сохраняем:
        gradient = np.zeros((image_height, image_width, 3), dtype=np.uint8)

        for y in range(image_height):
            height_deletion = y / image_height
            inv_height_deletion = 1 - height_deletion
            # вычисляем значение цвета на текущей строке на основе линейного градиента
            r = int(start_color[0] * inv_height_deletion + end_color[0] * height_deletion)
            g = int(start_color[1] * inv_height_deletion + end_color[1] * height_deletion)
            b = int(start_color[2] * inv_height_deletion + end_color[2] * height_deletion)

            # заполняем строку градиента
            gradient[y, :, :] = (b, g, r)  # OpenCV использует порядок BGR

        return gradient

    def draw_weather_card(self, image, name_of_window, data):
        image_height, image_width = image.shape[:2]
        window_height, window_width = self._get_window_sizes(image_height, image_width)

        # text_data будет не масштабируем - выходит за рамки задачи:
        text_data = data
        position = (20, 65)
        self._print_non_scale_text(image, text_data, position, 1)

        # text_content будет не масштабируем - выходит за рамки задачи:
        text_content = self.datas[data]['nune']['content']
        position = (300, 85)
        self._print_non_scale_text(image, text_content, position, 3)

        # text_weather масштабируем - в рамках доп. задания:
        text_weather = self.datas[data]['nune']['weather']
        self._print_scale_text(image, text_weather, image_height, image_width)

        # иконку, соответствующую погоде, рисуем на погодной карточке:
        icon = cv2.imread(self._choose_an_icon(data=data))
        icon_height, icon_width = icon.shape[:2]
        x_offset = (image_width - icon_width) // 2
        y_offset = (image_height - icon_height) // 2 + 10
        image[y_offset:(y_offset + icon_height), x_offset:(x_offset + icon_width)] = icon

        # добавляем градиент, соответствующий погоде:
        gradient = self._gradient_maker(data, image_height, image_width)
        image = cv2.addWeighted(image, 0.5, gradient, 0.5, 0)

        cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name_of_window, window_width, window_height)
        cv2.imshow(name_of_window, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run(self, datas):
        self.datas = datas  # важно в run() обновить значение self.datas, иначе другие функции не сработают
        for data in self.datas:
            image_cv2 = cv2.imread(self.form)
            self.draw_weather_card(image_cv2, name_of_window='Original version', data=data)


def print_dict_of_datas(datas):
    for data in datas:
        day, month = data.split(' of ')
        content = datas[data]['nune']['content']
        weather = datas[data]['nune']['weather']
        print(f'{day:>2} of {month:9}: {content:>3}, {weather}')
    print()


class ConsoleInterface:

    def __init__(self):
        self.continue_dialog = True
        self.datas = JSONDatabaseUpdater()
        self.full_dates_list = []
        for date_data in self.datas.return_data_for_all_days().values():
            self.full_dates_list.append(date_data['nune']['full_date'])

    def _all_days_in_console(self):
        print('Функция "все дни в консоли"')
        datas = self.datas.return_data_for_all_days()
        print_dict_of_datas(datas)

    def _five_days_in_console(self):
        print('Функция "ближайшие пять дней в консоли"')
        datas = self.datas.return_data_for_selected_days()
        print_dict_of_datas(datas)

    def _five_days(self):
        print('Функция "ближайшие пять дней на карточках"')
        datas_for_five_days = self.datas.return_data_for_selected_days()
        weather_cards = ImageMaker()
        weather_cards.run(datas_for_five_days)  # по полученному словарю дат рисуем карточки
        print()

    def _upload_data(self):
        print('Функция получения данных с сайта')
        get_weather = WeatherScraper()
        get_weather.fetch_data()  # получаем данные с сайта
        current_dict_of_weather = get_weather.return_the_final_dict()  # получаем чистовой словарь для передачи в БД

        self.datas.refresh_database(current_dict_of_weather,
                                    make_copy=False)  # передаем словарь в обновитель базы данных
        self.datas._get_datas_from_bd()  # обновляем значение self.datas, с которой работают другие функции
        print('База обновлена\n')

    def _update_old_type_database(self):
        print('Функция обновления типа данных в базе')
        self.datas.update_old_type_database()
        print('Данные переведены в новый формат\n')

    def _user_input_to_clear_date(self, text=''):
        while True:
            user_input = input(f'Введите {text}дату в формате дд.мм.гг ')
            pattern = r'([0]?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|1[012])\.2[34]'
            output_is_good = re.match(pattern, user_input)
            if output_is_good:
                d, m, y = user_input.split('.')
                clear_date = '20' + y + '-' + m + '-' + d
                break
            else:
                print('Некорректная дата!')
        return clear_date

    def _check_clear_date(self, text=''):
        while True:
            clear_date = self._user_input_to_clear_date(text)
            if clear_date in self.full_dates_list:
                break
            else:
                print('Такой даты нет в записях!')
        return clear_date

    def _get_period(self):
        print('Функция "погода за период"')
        while True:
            start_date = self._check_clear_date('начальную ')
            finish_date = self._check_clear_date('конечную ')
            if self.full_dates_list.index(start_date) <= self.full_dates_list.index(finish_date):
                break
            else:
                print('Конечная дата должна быть больше или равной начальной!')
        print()

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        finish_date_obj = datetime.strptime(finish_date, "%Y-%m-%d")

        selected_period = [date for date in self.full_dates_list if
                           start_date_obj <= datetime.strptime(date, "%Y-%m-%d") <= finish_date_obj]
        selected_period_str = [date_to_str_en_date(date) for date in selected_period]

        datas = self.datas.return_data_for_selected_days(selected_period_str)
        print_dict_of_datas(datas)

    def _upload_own_data(self):
        print('Функция загрузки своих данных')
        while True:
            start_date = self._user_input_to_clear_date('начальную')
            finish_date = self._user_input_to_clear_date('конечную')

            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            finish_date_obj = datetime.strptime(finish_date, "%Y-%m-%d")

            summ_of_days = (finish_date_obj - start_date_obj).days
            if start_date_obj > finish_date_obj:
                print('Конечная дата должна быть больше или равной начальной!\n')
            elif summ_of_days > 3:
                print('Период получился более 3-х дней. Вы замучаетесь вбивать...\n')
            else:
                break

        date_list = []
        current_date_obj = start_date_obj
        while current_date_obj <= finish_date_obj:
            date_list.append(current_date_obj.strftime('%Y-%m-%d'))
            current_date_obj += timedelta(days=1)
        print()

        # Для облегчения заполнения словаря ввод осуществляется только для 'nune'. Остальные времена заполнятся ничем
        new_weather_dict = {}
        for day in date_list:
            str_day = date_to_str_en_date(day)
            new_weather_dict[str_day] = {}

            day_obj = datetime.strptime(day, "%Y-%m-%d")
            wd = day_obj.strftime("%A")  # день недели

            content = input(f'Введите значение температуры на дату {str_day}, {wd}: ')
            weather = input(f'Введите описание погоды на дату {str_day}, {wd}: ')

            new_weather_dict[str_day]['night'] = {"weekday": wd, "content": '-', "weather": '-', "full_date": day}
            new_weather_dict[str_day]['morning'] = {"weekday": wd, "content": '-', "weather": '-', "full_date": day}
            new_weather_dict[str_day]['nune'] = {
                "weekday": wd,
                "content": content,
                "weather": weather,
                "full_date": day
            }
            new_weather_dict[str_day]['evening'] = {"weekday": wd, "content": '-', "weather": '-', "full_date": day}
            print()

        self.datas.refresh_database(new_weather_dict, make_copy=True)

    def _exit(self):
        print('До встречи!')
        self.continue_dialog = False

    def main(self):
        print('Приветствуем тебя, юзернейм! Это программа парсинга погоды!')
        all_funtion_in_that_class = [
            ['Распечатать прогноз на все дни', self._all_days_in_console],
            ['Распечатать прогноз на 5 дней в консоли', self._five_days_in_console],
            ['Распечатать прогноз на 5 дней на карточках', self._five_days],
            ['Загрузить новые данные с сайта', self._upload_data],
            # ['Обновить тип данных в старых датах', self._update_old_type_database],
            ['Выгрузить данные за диапазон дат', self._get_period],
            ['Вбить свои данные за диапазон дат', self._upload_own_data],
            ['Выход', self._exit],
        ]
        options = {}
        for i, func in enumerate(all_funtion_in_that_class):
            options[str(i + 1)] = func

        while self.continue_dialog:
            while True:
                print('Выберете действие:')
                for num in options:
                    print(f'{num}: {options[num][0]}')

                user_input = input(f'Введите номер [1-{len(options)}] ')
                print()
                if user_input in options.keys():
                    options[user_input][1]()
                    break
                else:
                    print("Неверный ввод\n")


if __name__ == "__main__":
    dialog = ConsoleInterface()
    dialog.main()

    current_weather_dict = dialog.datas.return_data_for_all_days()
    save_weather_data(current_weather_dict)

    all_weather_data = WeatherData.select()
    print('Получение данных из модели для всех записей:')
    for data in all_weather_data:
        # pprint(data.__data__.items())
        for key, value in data.__data__.items():
            print(f"{key:}: {value:4}", end=', ')
        print()
    print('~' * 150)

    print('Получение данных из модели с фильтром на day и time:')
    specific_date = '13 of October'
    weather_data_for_specific_date = WeatherData.select().where(
        WeatherData.day == specific_date,
        # WeatherData.time == 'nune'
    )
    for data in weather_data_for_specific_date:
        print(specific_date, ':', data.content, ', ', data.weather)
    print('~' * 150)

    print('Получение данных из модели для конкретной даты (первая найденная запись):')
    specific_date = '2023-10-01'
    data_for_specific_date = WeatherData.get(WeatherData.full_date == specific_date)
    print(specific_date, ':', data_for_specific_date.content, ', ', data_for_specific_date.weather)


# запуск в консоли: C:\Users\Ivan\PyCharm\SkillBox\lesson_016\venv\Scripts\Python.exe C:\Users\Ivan\PyCharm\SkillBox\lesson_016\00_weather.py
