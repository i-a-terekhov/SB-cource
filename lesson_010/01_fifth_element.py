# -*- coding: utf-8 -*-

# Умножить константу BRUCE_WILLIS на пятый элемент строки, введенный пользователем

def ExceptKipper(exception):
    if exception == IndexError:
        print(f'Получили ошибку {str(type(exception)).split()[1][:-1]}: {exception}')
        print('Количество символов недостаточно')
    elif exception == ValueError:
        print(f'Получили ошибку {str(type(exception)).split()[1][:-1]}: {exception}')
        print('Получен символ, ожидалось число')
    elif exception == BaseException:
        print(f'Получили ошибку {str(type(exception)).split()[1][:-1]}: {exception}')


BRUCE_WILLIS = 42

input_data = input('Если хочешь что-нибудь сделать, сделай это сам: ')
try:
    leeloo = int(input_data[4])
    result = BRUCE_WILLIS * leeloo
    print(f"- Leeloo Dallas! Multi-pass № {result}!")
except BaseException:
    ExceptKipper(exception=BaseException)

# Ообернуть код и обработать исключительные ситуации для произвольных входных параметров
# - ValueError - невозможно преобразовать к числу
# - IndexError - выход за границы списка
# - остальные исключения
# для каждого типа исключений написать на консоль соотв. сообщение




