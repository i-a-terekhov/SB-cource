# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234

class LogAnalysis:
    """Класс-генератор для анализа лога событий по часам, месяцам, году"""

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = {}

    def _open(self):
        return open(self.file_name, 'r', encoding='utf8')

    def _type_of_sort(self):
        user_type = 'minute'
        self.sort_type = {
            'minute': (1, 17),
            'hour': (1, 14),
            'day': (1, 11),
            'month': (1, 8),
            'year': (1, 5),
        }
        return self.sort_type[user_type]

    def __iter__(self):
        with self._open() as file_obj:
            a, b = self._type_of_sort()
            time_of_past_step = file_obj.readline()[a:b]

            for string in file_obj:
                time = string[a:b]

                if time != time_of_past_step:
                    yield time_of_past_step, self.stat.get(time_of_past_step, 0)

                status = string[29:-1]
                if status == 'NOK':
                    if time in self.stat:
                        self.stat[time] += 1
                    else:
                        self.stat[time] = 1

                time_of_past_step = time


file_for_analysis = 'events.txt'
grouped_events = LogAnalysis(file_name=file_for_analysis)
for group_time, event_count in grouped_events:
    print(f'[{group_time}] {event_count}')
