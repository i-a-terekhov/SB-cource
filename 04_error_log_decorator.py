# -*- coding: utf-8 -*-

# Написать декоратор, который будет логировать (записывать в лог файл)
# ошибки из декорируемой функции и выбрасывать их дальше.
#
# Имя файла лога - function_errors.log
# Формат лога: <имя функции> <параметры вызова> <тип ошибки> <текст ошибки>
# Лог файл открывать каждый раз при ошибке в режиме 'a'

import time


def log_errors(log_file_name):
    def log_file_choser(func):
        def log_writter(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                with open(log_file_name, 'a') as log:
                    log.write(
                        f'{time.strftime("%x %X", time.gmtime())} An error occurred in function {func.__name__}: {str(e)}\n')
                raise
            return result

        return log_writter

    return log_file_choser


# Проверить работу на следующих функциях
@log_errors(log_file_name='log_file_for_perky.txt')
def perky(param):
    return param / 0


@log_errors(log_file_name='log_file_for_check_line.txt')
def check_line(line):
    name, email, age = line.split(' ')
    if not name.isalpha():
        raise ValueError("it's not a name")
    if '@' not in email or '.' not in email:
        raise ValueError("it's not a email")
    if not 10 <= int(age) <= 99:
        raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]
for line in lines:
    try:
        check_line(line)
    except Exception as exc:
        print(f'Invalid format: {exc}')

try:
    perky(param=42)
except Exception as exc:
    print(f'Invalid format: {exc}')

# Усложненное задание (делать по желанию).
# Написать декоратор с параметром - именем файла
#
# @log_errors('function_errors.log')
# def func():
#     pass
