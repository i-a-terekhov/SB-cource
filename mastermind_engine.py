import random
from termcolor import cprint

_hidden_number = []
_number_from_user = []


def save_hidden_number():
    while len(_hidden_number) < 4:
        candidate = random.randint(1, 9)
        if candidate not in _hidden_number:
            _hidden_number.append(candidate)


def save_str_to_list(input_from_user: str):
    for i in input_from_user:
        _number_from_user.append(int(i))


def check_the_input_and_save(input_from_user: str):
    cprint('Пользователь ввел ', end='', color='green')
    cprint(input_from_user, end='', color='yellow')
    cprint(' ', end='')

    try:
        input_from_user = int(input_from_user)
    except ValueError:
        cprint('Введенное значение не является числом', color='red')
        return False

    if input_from_user > 9999 or input_from_user < 1111:
        cprint('Число не входит в диапазон', color='red')
        return False
    else:
        cprint('Проверяем:', color='green')
        save_str_to_list(str(input_from_user))
        return True


def compare_user_number_with_hidden_one():
    answer = {'bulls': 0, 'cows': 0}
    for i in range(4):
        if _hidden_number[i] in _number_from_user:
            answer['cows'] += 1
        if _hidden_number[i] == _number_from_user[i]:
            answer['bulls'] += 1
            answer['cows'] -= 1
    _number_from_user.clear()
    return answer


def mach(answer: dict):
    if answer.get('bulls') == 4:
        return True
    else:
        return False
