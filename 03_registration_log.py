# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.

class NotNameError(Exception):

    def __str__(self):
        return 'Поле Имя содержит символы, отличные от букв'


class NotEmailError(Exception):

    def __str__(self):
        return 'Email не содержит обязательных символов из набора (@, точка)'


good_log = 'registrations_good.log'
bad_log = 'registrations_bad.log'

with open('registrations.txt', 'r', encoding='utf-8') as log_file:
    for line in log_file:
        is_errors = False
        user_data = line.split()

        if len(user_data) != 3:
            print(f'В строке <{line[:-1]:^35}> не хватает данных')
            is_errors = True
            # raise ValueError
        else:
            name, email, age = user_data

            if not name.isalpha():
                print(f'В строке <{line[:-1]:^35}> некорректно значение <  {name:^15} >')
                is_errors = True
                # raise NotNameError

            if '.' not in email or '@' not in email:
                print(f'В строке <{line[:-1]:^35}> некорректно значение < {email:^15} >')
                is_errors = True
                # raise NotEmailError

            try:
                age = int(age)
                if not 10 < age < 99:
                    print(f'В строке <{line[:-1]:^35}> некорректно значение < {age:^15} >')
                    is_errors = True
                    # raise ValueError
            except ValueError:
                print(f'В строке <{line[:-1]:^35}> некорректно значение < {age:^15} >')
                is_errors = True
                # raise ValueError

        if is_errors:
            with open(bad_log, 'a') as log:
                log.write(line)
        else:
            with open(good_log, 'a') as log:
                log.write(line)

