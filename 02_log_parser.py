# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import os


class LogAnalysis:
    """Класс анализа лога событий по часам, месяцам, году"""

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = {}
        self.stat_list = []
        self.out_file_name = 'NOK_stat'

    def _open(self):
        file_size = os.stat(self.file_name).st_size
        print('Объем текущего файла статистики', file_size, 'Кб')
        return open(self.file_name, 'r', encoding='utf8')

    def _type_of_sort(self):
        self.sort_type = {
            'minute': (1, 17),
            'hour': (1, 14),
            'day': (1, 11),
            'month': (1, 8),
            'year': (1, 5),
        }
        user_type = 'day'
        return self.sort_type[user_type]

    def get_stat(self):
        with self._open() as file_obj:
            a, b = self._type_of_sort()
            for string in file_obj:
                time = string[a:b]
                status = string[29:-1]
                if status == 'NOK':
                    if time in self.stat:
                        self.stat[time] += 1
                    else:
                        self.stat[time] = 1
        self.stat_list = sorted(self.stat.items(), key=lambda x: x[0])
        for time in self.stat_list:
            print(f'[{time[0]}] {time[1]}')

    def safe_stat(self):
        with open(self.out_file_name, 'w', encoding='utf8') as file:
            for time in self.stat_list:
                file.write(f'[{time[0]}] {time[1]}\n')


file_for_analysis = 'events.txt'
Analysis = LogAnalysis(file_name=file_for_analysis)
Analysis.get_stat()
Analysis.safe_stat()

# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
