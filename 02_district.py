# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join

import district.central_street.house1.room1 as room1
import district.central_street.house1.room2
import district.central_street.house2.room1 as room3
import district.central_street.house2.room2
from district.soviet_street.house1 import room1 as room5        # имя room1 уже занято!
from district.soviet_street.house1.room2 import folks           # импорт конкретной переменной
from district.soviet_street.house2.room1 import folks as folk07
from district.soviet_street.house2.room2 import folks as folk08

# for street in dir(district):
#     print('Вывод метода', street, ':')
#     print(eval('district.' + street))
#     print()
# print('ИТОГО, методы данного модуля:')
# print(', '.join(dir(district)))

citizen = []
for folk in [
    room1.folks,
    district.central_street.house1.room2.folks,
    room3.folks,
    district.central_street.house2.room2.folks,
    room5.folks,
    folks,
    folk07,
    folk08
]:
    citizen.extend(folk)
print(citizen)