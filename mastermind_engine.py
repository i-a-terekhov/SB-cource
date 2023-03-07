# Правила:
# Компьютер загадывает четырехзначное число, все цифры которого различны
# (первая цифра числа отлична от нуля). Игроку необходимо разгадать задуманное число.
# Игрок вводит четырехзначное число c неповторяющимися цифрами,
# компьютер сообщают о количестве «быков» и «коров» в названном числе
# «бык» — цифра есть в записи задуманного числа и стоит в той же позиции,
#       что и в задуманном числе
# «корова» — цифра есть в записи задуманного числа, но не стоит в той же позиции,
#       что и в задуманном числе
#
# Например, если задумано число 3275 и названо число 1234,
# получаем в названном числе одного «быка» и одну «корову».
# Очевидно, что число отгадано в том случае, если имеем 4 «быка».
#
# Формат ответа компьютера
# > быки - 1, коровы - 1

# В этом модуле нужно реализовать функции:
#   загадать_число()
#   проверить_число(NN) - возвращает словарь {'bulls': N, 'cows': N}
# Загаданное число хранить в глобальной переменной.
# Обратите внимание, что строки - это список символов.

import random

_hidden_number = []


def make_a_number():
    while len(_hidden_number) < 4:
        candidate = random.randint(1, 9)
        if candidate not in _hidden_number:
            _hidden_number.append(candidate)
    return _hidden_number


def check_the_number(number_from_the_user: str):
    print('Пользователь ввел', end='')
    print(number_from_the_user)
    # TODO преобразовать number_from_the_user в list

    # TODO сравнить list number_from_the_user с загаданным

    # TODO выдать результат сравнения (быки и коровы)

print(make_a_number())
check_the_number(input('Введите что-нибудь '))

