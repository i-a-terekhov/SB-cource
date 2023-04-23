# -*- coding: utf-8 -*-

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.

import random


class IamGodError(Exception):

    def __str__(self):
        return 'Ошибка бога'


class DrunkError(Exception):

    def __str__(self):
        return 'Синька-чмо'


class CarCrashError(Exception):

    def __str__(self):
        return 'Машина разбита'


class GluttonyError(Exception):

    def __str__(self):
        return 'Набитие требухи'


class DepressionError(Exception):

    def __str__(self):
        return 'Депрессия'


class SuicideError(Exception):

    def __str__(self):
        return 'Суицидальность'


ENLIGHTENMENT_CARMA_LEVEL = 777


def one_day():
    if random.randint(1, 2) == 1:
        errors = [IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError]
        which_error = random.randint(0, len(errors) - 1)
        raise errors[which_error]
    return random.randint(1, 7)


def except_processor(exception):

    if isinstance(exception, IamGodError):
        return "Oh no, someone thinks they're God!"
    elif isinstance(exception, DrunkError):
        return "Looks like someone's had too much to drink..."
    elif isinstance(exception, CarCrashError):
        return "There's been a car crash, are you alright?"
    elif isinstance(exception, GluttonyError):
        return "Slow down there, you're going to make yourself sick!"
    elif isinstance(exception, DepressionError):
        return "It's okay to not be okay, let's talk about it."
    elif isinstance(exception, SuicideError):
        return "Please don't do anything drastic, there is always help available."
    else:
        return "Unknown cause...", exception


def log_update(day, exception, answer):
    with open('Log_of_carmas.txt', 'a') as log:
        log.write(
            f'Day {str(day):3} - Except: {exception.__str__():15} - Processor answer: {answer}'
        )
        log.write('\n')


day = 0
current_carma = 0
while current_carma < ENLIGHTENMENT_CARMA_LEVEL:
    day += 1

    try:
        carma_today = one_day()
        current_carma += carma_today
        print(f'День {day}, сегодняшняя карма равна {carma_today}, всего уровень кармы достиг отметки {current_carma}')
    except BaseException as e:
        print(f'День {day}, сегодня карма не повысилась, уровень кармы остался на отметке {current_carma}')
        except_processor_answer = except_processor(exception=e)
        log_update(day=day, exception=e, answer=except_processor_answer)


# https://goo.gl/JnsDqu
