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

# TODO здесь ваш код
import zipfile
from pprint import pprint

from termcolor import cprint

work_with = 'voyna-i-mir.txt.zip'
file_name = 'voyna-i-mir.txt'

alfavit = {}

if work_with.endswith('zip'):
    zfile = zipfile.ZipFile(work_with, 'r')
    for name in zfile.namelist():
        if name == 'voyna-i-mir.txt':
            zfile.extract(name)

with open(file_name, 'r', encoding='cp1251') as file:
    for line in file:
        for char in line:
            if char.isalpha():
                if char in alfavit:
                    alfavit[char] += 1
                else:
                    alfavit[char] = 1


sort_list = sorted(alfavit.items(), key=lambda item: item[1], reverse=True)
sum = 0
print('+{:-^8}+{:-^10}+'.format('', ''))
print('|{:^8}|{:^10}|'.format('Буква', 'Частота'))
print('+{:-^8}+{:-^10}+'.format('', ''))
for i in sort_list:
    print('|{:^8}|{:^10}|'.format(i[0], i[1]))
    sum += i[1]
print('+{:-^8}+{:-^10}+'.format('', ''))
print('|{:^8}|{:^10}|'.format('Итого', sum))
print('+{:-^8}+{:-^10}+'.format('', ''))

# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
