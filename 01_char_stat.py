# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import zipfile
import os


class Chatter:
    """Класс генератора текста на основе изученных файлов"""

    alphabet = {}
    sort_stat = []

    def __init__(self, file_name):
        self.file_name = file_name
        self.out_file_name = 'out.txt'

    def unzip(self):
        if self.file_name.endswith('zip'):
            archived_file = zipfile.ZipFile(self.file_name, 'r')
            for name in archived_file.namelist():
                if name.endswith('txt'):
                    archived_file.extract(name)
        self._connecting_txt_files()

    def _connecting_txt_files(self):
        open_mode = 'a'
        if os.path.isfile(self.out_file_name):
            file_size = os.stat(self.out_file_name).st_size
            print('Объем текущего файла статистики', file_size, 'Кб')
            if file_size > 15_000_000:
                print('Обнуляем файл статистики')
                open_mode = 'w'
        else:
            print('Создаем файл статистики')
        out_file = open(self.out_file_name, open_mode, encoding='utf8')

        for name in os.listdir('.'):
            if name.endswith('txt') and name != self.out_file_name:
                print('Найден файл: ', name)
                with open(name, 'r') as text:
                    out_file.write(text.read())
                out_file.write('\n')
        out_file.close()

    def get_statistic(self, *args):
        with open(self.out_file_name, 'r', encoding='utf8') as file:
            for line in file:
                for char in line:
                    if char.isalpha():
                        if char in self.alphabet:
                            self.alphabet[char] += 1
                        else:
                            self.alphabet[char] = 1
        self._sort(*args)
        self._print_stat()

    def _sort(self, selected_method='alphabet_reverse'):
        sorting_methods = {
            'frequency_reverse': [1, True],
            'frequency': [1, False],
            'alphabet': [0, False],
            'alphabet_reverse': [0, True]
        }
        self.sort_stat = sorted(
            self.alphabet.items(),
            key=lambda symbol: symbol[sorting_methods[selected_method][0]],
            reverse=sorting_methods[selected_method][1]
        )

    def _print_stat(self):
        sum = 0
        print('+{:-^8}+{:-^10}+'.format('', ''))
        print('|{:^8}|{:^10}|'.format('Буква', 'Частота'))
        print('+{:-^8}+{:-^10}+'.format('', ''))
        for i in self.sort_stat:
            print('|{:^8}|{:^10}|'.format(i[0], i[1]))
            sum += i[1]
        print('+{:-^8}+{:-^10}+'.format('', ''))
        print('|{:^8}|{:^10}|'.format('Итого', sum))
        print('+{:-^8}+{:-^10}+'.format('', ''))


file_for_analysis = 'voyna-i-mir.txt.zip'
chatter = Chatter(file_name=file_for_analysis)
chatter.unzip()
chatter.get_statistic('frequency')

# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
