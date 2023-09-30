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
from datetime import datetime


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

    def return_the_final_dict(self):
        if len(self.weather_row_data) > 0:
            self._create_weather_dict()
            return self.new_weather_dict
        else:
            raise Exception('Словарь текущей погоды не сформирован')


class DatabaseUpdater:
    def __init__(self):
        self.database_name = r'C:\Users\Ivan\PyCharm\SkillBox\lesson_016\weather_dict.json'
        self.weather_data = None

    def refresh_database(self, new_weather_dict):
        with open(self.database_name, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)

        existing_data.update(new_weather_dict)

        with open(self.database_name, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    def _get_datas_from_bd(self):
        with open(self.database_name, 'r', encoding='utf-8') as file:
            self.weather_data = json.load(file)

    def return_data_for_selected_days(self, days=None):
        if not self.weather_data:
            self._get_datas_from_bd()

        def str_date_to_date(date_str):
            parts = date_str.split(' of ')
            day = int(parts[0])
            month = datetime.strptime(parts[1], '%B').month
            return datetime(today.year, month, day).date()

        data_for_selected_days = {}
        date_list = self.weather_data.keys()
        if days is None:
            today = datetime.now().date()
            max_weather_cards = 5
            selected_dates = 0
            for date_str in date_list:
                date = str_date_to_date(date_str)
                if date >= today:
                    selected_dates += 1
                    data_for_selected_days[date_str] = self.weather_data[date_str]
                if selected_dates >= max_weather_cards:
                    break
        else:
            for day in days:
                if day in date_list:
                    data_for_selected_days[day] = self.weather_data[day]
        print(f'Доступен прогноз на следующие дни: {list(data_for_selected_days.keys())}')
        return data_for_selected_days


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
        self.datas = datas
        for data in datas:
            image_cv2 = cv2.imread(self.form)
            content = self.datas[data]['nune']['content']
            weather = self.datas[data]['nune']['weather']
            print(f'{data}: {content}, {weather}')
            self.draw_weather_card(image_cv2, name_of_window='Original version', data=data)


class ConsoleInterface:
    def __init__(self):
        self.continue_dialog = True

    def _five_days(self):
        print('Функция ближайшие пять дней')
        datas_getter = DatabaseUpdater()
        datas_for_five_days = datas_getter.return_data_for_selected_days()
        weather_cards = ImageMaker()
        weather_cards.run(datas_for_five_days) # по полученному словарю выбранных дат обращаемся отрисовываем содержание
        print()

    def _upload_data(self):
        print('Функция получения данных с сайта')
        get_weather = WeatherScraper()
        get_weather.fetch_data()  # получаем данные с сайта
        current_dict_of_weather = get_weather.return_the_final_dict()  # получаем чистовой словарь для передачи в БД

        db_updater = DatabaseUpdater()
        db_updater.refresh_database(current_dict_of_weather)  # передаем словарь в обновитель базы данных
        print('База обновлена\n')

    def _exit(self):
        print('До встречи!')
        self.continue_dialog = False

    def main(self):
        print('Приветствуем тебя, юзернейм! Это программа парсинга погоды!')

        while self.continue_dialog:
            options = {
                '1': ['Распечатать прогноз на 5 дней', self._five_days],
                '2': ['Загрузить новые данные с сайта', self._upload_data],
                '3': ['Выход', self._exit]
            }
            while True:
                print('Выберете действие:')
                for num in options:
                    print(f'{num}: {options[num][0]}')

                user_input = input(f'Введите номер [1-{len(options)}] ')

                if user_input in options.keys():
                    options[user_input][1]()
                    break
                else:
                    print("Неверный ввод\n")


if __name__ == "__main__":
    dialog = ConsoleInterface()
    dialog.main()

# запуск в консоли: C:\Users\Ivan\PyCharm\SkillBox\lesson_016\venv\Scripts\Python.exe C:\Users\Ivan\PyCharm\SkillBox\lesson_016\00_weather.py

#TODO
# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.