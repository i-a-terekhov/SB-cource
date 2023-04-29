# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел
# import time
#
#
# def get_prime_numbers(n):
#     prime_numbers = []
#     timeofstart = time.time()
#     timezero = time.time()
#     for number in range(2, n+1):
#         for prime in prime_numbers:
#             if number % prime == 0:
#                 break
#         else:
#             prime_numbers.append(number)
#             timeend = time.time()
#             print(f'{number:10} - {round(((timeend-timezero)*1_000_000)):7} - {round(((timeend-timeofstart)*1)):5}')
#             timezero = timeend
#     return prime_numbers

# print(get_prime_numbers(1_000))

# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:

    def __init__(self, n):
        self.n = n
        self.prime_numbers = []
        self.is_print_all = True

    def g_print(self, text, print_all=False):
        if print_all is True:
            print(text)

    def __iter__(self):
        self.i = 2
        return self

    def __next__(self):
        self.g_print('-' * 100, self.is_print_all)
        while self.i <= self.n:
            self.g_print(f'Рассматриваем число {self.i}', self.is_print_all)
            for prime in self.prime_numbers:
                self.g_print(f'Берем число {prime} из последовательности {self.prime_numbers}', self.is_print_all)
                self.g_print(f'Делим нацело {self.i} на {prime}, получаем результат {self.i % prime}',
                             self.is_print_all)
                if self.i % prime == 0:
                    self.g_print(f'Число {self.i} нацело разделилось на {prime} - такое нам не подходит',
                                 self.is_print_all)
                    break
            else:
                self.g_print(f'Добавляем число {self.i} в лист {self.prime_numbers}', self.is_print_all)
                self.prime_numbers.append(self.i)
                result = self.i
                self.i += 1
                return result
            self.i += 1
        raise StopIteration()


prime_number_iterator = PrimeNumbers(n=1000)
for number in prime_number_iterator:
    print(number)


# TODO после подтверждения части 1 преподователем, можно делать
# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


def prime_numbers_generator(n):
    pass
    # TODO здесь ваш код

# for number in prime_numbers_generator(n=10000):
#     print(number)


# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.
