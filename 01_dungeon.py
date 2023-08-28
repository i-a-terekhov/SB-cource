# -*- coding: utf-8 -*-

# С помощью JSON файла rpg.json задана "карта" подземелья.
# Подземелье было выкопано монстрами и они всё ещё скрываются где-то в его глубинах,
# планируя набеги на близлежащие поселения.
# Само подземелье состоит из двух главных разветвлений и нескольких развилок,
# и лишь один из путей приведёт вас к главному Боссу
# и позволит предотвратить набеги и спасти мирных жителей.

# Напишите игру, в которой пользователь, с помощью консоли,
# сможет:
# 1) исследовать это подземелье:
#   -- передвижение должно осуществляться присваиванием переменной и только в одну сторону
#   -- перемещаясь из одной локации в другую, пользователь теряет время, указанное в конце названия каждой локации
# Так, перейдя в локацию Location_1_tm500 - вам необходимо будет списать со счёта 500 секунд.
# Тег, в названии локации, указывающий на время - 'tm'.
#
# 2) сражаться с монстрами:
#   -- сражение имитируется списанием со счета персонажа N-количества времени и получением N-количества опыта
#   -- опыт и время указаны в названиях монстров (после exp указано значение опыта и после tm указано время)
# Так, если в локации вы обнаружили монстра Mob_exp10_tm20 (или Boss_exp10_tm20)
# необходимо списать со счета 20 секунд и добавить 10 очков опыта.
# Теги указывающие на опыт и время - 'exp' и 'tm'.
# После того, как игра будет готова, сыграйте в неё и наберите 280 очков при положительном остатке времени.

# По мере продвижения вам так же необходимо вести журнал,
# в котором должна содержаться следующая информация:
# -- текущее положение
# -- текущее количество опыта
# -- текущая дата (отсчёт вести с первой локации с помощью datetime)
# После прохождения лабиринта, набора 280 очков опыта и проверки на остаток времени (remaining_time > 0),
# журнал необходимо записать в csv файл (назвать dungeon.csv, названия столбцов взять из field_names).

# Пример лога игры:
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 1234567890.0987654321 секунд
# Прошло уже 0:00:00
# Внутри вы видите:
# -- Монстра Mob_exp10_tm0
# -- Вход в локацию: Location_1_tm10400000
# -- Вход в локацию: Location_2_tm333000000
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Выход

remaining_time = '1234567890.0987654321'
# если изначально не писать число в виде строки - теряется точность!
field_names = ['current_location', 'current_experience', 'current_date']

import json
from pprint import pprint


with open("rpg.json", "r") as rpg_file:
    rpg_data = json.load(rpg_file)
    # print('Полученный json преобразован в объект', type(rpg_data))  # <class 'dict'>

# rpg_dumps = json.dumps(rpg_data)  # dumps - запись в переменную в виде строки <- памятка
# print(type(rpg_dumps))

current_location = rpg_data
current_location_name = list(current_location.keys())[0]
game_over = False
while not game_over:
    print(f'Вы находитесь в {current_location_name}')
    location_content = current_location[current_location_name]
    location_num_in_list = 0
    next_step_locations = {}
    next_loc_exist = True
    monster_attack = False
    print('Внутри вы видите:')
    for entity in location_content:
        if isinstance(entity, str):
            print(f'-- Монстра: {entity}')
            monster_attack = True
        elif isinstance(entity, list):
            print('-- Группу монстров: ', end='')
            for _ in entity:
                print(_, end=' ')
            print()
            monster_attack = True
        else:
            one_of_locations = list(entity.keys())[0]
            next_step_locations[one_of_locations] = location_num_in_list
        location_num_in_list += 1

    if len(next_step_locations) == 0:
        print('Вы в тупике')
        next_loc_exist = False
        game_over = True
    else:
        locations = list(next_step_locations.keys())
        for location in locations:
            print(f'-- Вход в локацию {location}')

    print('Выберите действие:')
    if monster_attack:
        print('Атаковать монстра')
    if next_loc_exist:
        print('Перейти в другую локацию')

    if next_loc_exist:
        new_loc = list(next_step_locations.items())[0]
        print('Вы выбрали локацию:')
        print(new_loc)
        current_location = location_content[new_loc[1]]
        current_location_name = list(current_location.keys())[0]
        print('-' * 20)

# with open("rpg2.json", "w") as write_file:
#     json.dump(rpg_data, write_file, indent=2)  # dump - запись в переменную
#     # print('Полученный объект', type(rpg_data), 'преобразован в json')

