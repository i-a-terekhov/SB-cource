# Есть словарь кодов товаров
goods = {
    'Лампа': '12345',
    'Стол': '23456',
    'Диван': '34567',
    'Стул': '45678',
}

# Есть словарь списков количества товаров на складе.
store = {
    '12345': [
        {'quantity': 27, 'price': 42},
    ],
    '23456': [
        {'quantity': 22, 'price': 510},
        {'quantity': 32, 'price': 520},
    ],
    '34567': [
        {'quantity': 2, 'price': 1200},
        {'quantity': 1, 'price': 1150},
    ],
    '45678': [
        {'quantity': 50, 'price': 100},
        {'quantity': 12, 'price': 95},
        {'quantity': 43, 'price': 97},
    ],
}

# Рассчитать на какую сумму лежит каждого товара на складе
# например для ламп
#
# lamps_cost = store[goods['Лампа']][0]['quantity'] * store[goods['Лампа']][0]['price']
# # или проще (/сложнее ?)
# lamp_code = goods['Лампа']
# lamps_item = store[lamp_code][0]
# lamps_quantity = lamps_item['quantity']
# lamps_price = lamps_item['price']
# lamps_cost = lamps_quantity * lamps_price
# print('Лампа -', lamps_quantity, 'шт, стоимость', lamps_cost, 'руб')

# Вывести стоимость каждого товара на складе: один раз распечать сколько всего столов, стульев и т.д. на складе
# Формат строки <товар> - <кол-во> шт, стоимость <общая стоимость> руб

# WARNING для знающих циклы: БЕЗ циклов. Да, с переменными; да, неэффективно; да, копипаста.
# Это задание на ручное вычисление - что бы потом понять как работают циклы и насколько с ними проще жить.

lamp_quan_00 = store[goods['Лампа']][0]['quantity']
lamp_cost_00 = lamp_quan_00 * store[goods['Лампа']][0]['price']
lamp_cost_all = lamp_cost_00
lamp_quan_all = lamp_quan_00
print('Лампа -', lamp_quan_all, 'шт, стоимость', lamp_cost_all, 'руб')

table_quan_00 = store[goods['Стол']][0]['quantity']
table_cost_00 = table_quan_00 * store[goods['Стол']][0]['price']
table_quan_01 = store[goods['Стол']][1]['quantity']
table_cost_01 = table_quan_01 * store[goods['Стол']][1]['price']
table_cost_all = table_cost_00 + table_cost_01
table_quan_all = table_quan_00 + table_quan_01
print('Стол -', table_quan_all, 'шт, стоимость', table_cost_all, 'руб')

couch_quan_00 = store[goods['Диван']][0]['quantity']
couch_cost_00 = couch_quan_00 * store[goods['Диван']][0]['price']
couch_quan_01 = store[goods['Диван']][1]['quantity']
couch_cost_01 = couch_quan_01 * store[goods['Диван']][1]['price']
couch_cost_all = couch_cost_00 + couch_cost_01
couch_quan_all = couch_quan_00 + couch_quan_01
print('Диван -', couch_quan_all, 'шт, стоимость', couch_cost_all, 'руб')

chair_quan_00 = store[goods['Стул']][0]['quantity']
chair_cost_00 = chair_quan_00 * store[goods['Стул']][0]['price']
chair_quan_01 = store[goods['Стул']][1]['quantity']
chair_cost_01 = chair_quan_01 * store[goods['Стул']][1]['price']
chair_quan_02 = store[goods['Стул']][2]['quantity']
chair_cost_02 = chair_quan_02 * store[goods['Стул']][2]['price']
chair_cost_all = chair_cost_00 + chair_cost_01 + chair_cost_02
chair_quan_all = chair_quan_00 + chair_quan_01 + chair_quan_02
print('Стул -', chair_quan_all, 'шт, стоимость', chair_cost_all, 'руб')

##########################################################################################
# ВНИМАНИЕ! После того как __ВСЯ__ домашняя работа сделана и запушена на сервер,         #
# нужно зайти в ЛМС (LMS - Learning Management System ) по адресу http://go.skillbox.ru  #
# и оформить попытку сдачи ДЗ! Без этого ДЗ не будет проверяться!                        #
# Как оформить попытку сдачи смотрите видео - https://youtu.be/qVpN0L-C3LU               #
##########################################################################################






