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

# remaining_time = '1234567890.0987654321'
# если изначально не писать число в виде строки - теряется точность!
# field_names = ['current_location', 'current_experience', 'current_date']

import json
from pprint import pprint
import time
import re

with open("rpg.json", "r") as rpg_file:
    rpg_data = json.load(rpg_file)
    # print('Полученный json преобразован в объект', type(rpg_data))  # <class 'dict'>

# rpg_dumps = json.dumps(rpg_data)  # dumps - запись в переменную в виде строки <- памятка
# print(type(rpg_dumps))


def time_cost(text_name: str):
    pattern = r'tm(\d+)'
    match = re.search(pattern, text_name)
    if match:
        return match.group(1)
    else:
        return None


def exp_calc(text_name: str):
    pattern = r'exp(\d+)'
    match = re.search(pattern, text_name)
    if match:
        return match.group(1)
    else:
        return None


current_location = rpg_data
current_location_name = list(current_location.keys())[0]
remaining_time = '1234567890.0987654321'
current_experience = 0
game_over = False
while not game_over:
    location_content = current_location[current_location_name]
    tree_of_options = []
    monster_exist = False
    next_loc_exist = False
    for num, entity in enumerate(location_content):
        if isinstance(entity, str):
            monster_exist = True
            name = entity
            cl = 'monster'
            action_time = time_cost(entity)
            exp = exp_calc(name)
        elif isinstance(entity, list):
            monster_exist = True
            name = ', '.join(entity)
            cl = 'monster'
            action_time = 0
            exp = 0
            for _ in entity:
                time += time_cost(_)
                exp += exp_calc(_)
        else:
            next_loc_exist = True
            name = list(entity.keys())[0]
            cl = 'entrance'
            action_time = time_cost(name)
            exp = exp_calc(name)
        tree_of_options.append(({'name': name, 'class': cl, 'time': action_time, 'exp': exp, 'address': num}))
    print('Итог скана локации')
    pprint(tree_of_options)

    user_action = ''
    answer_is_correct = False
    while not answer_is_correct:
        print('Выберите действие:')
        if monster_exist:
            print('1. Атаковать монстра')
        if next_loc_exist:
            print('2. Перейти в другую локацию')
        print('3. Выход')

        user_action = input()
        if user_action == '1' and monster_exist:
            answer_is_correct = True
        elif user_action == '2' and next_loc_exist:
            answer_is_correct = True
        elif user_action == '3':
            print('Вы решили завершить игру')
            game_over = True
            break
        else:
            print('Некорректный ввод')

    if user_action == '1':
        answer_is_correct = False
        while not answer_is_correct:
            print('Вы решили атаковать! Выберете цель!')
            num_of_monster = -1
            for monster in location_content:
                # TODO Баг: num_of_monster будет работать некорректно, если где-то перед монстрами будет локация
                if isinstance(monster, str):
                    num_of_monster += 1
                    print(f'{num_of_monster + 1} - {monster}')
                if isinstance(monster, list):
                    num_of_monster += 1
                    print(f'{num_of_monster + 1} - группа:', end=' ')
                    group = ', '.join(monster)
                    print(group)

            user_try_attack = input()
            try:
                user_try_attack = int(user_try_attack)
            except ValueError:
                print('Некорректный ввод')
                time.sleep(1)
                continue

            user_try_attack -= 1
            if user_try_attack not in [0, num_of_monster]:
                print('Промах!')
            else:
                monster_under_attack = location_content[user_try_attack]
                remaining_time = float(remaining_time)
                time_for_fight = 0.0
                experience = 0
                if isinstance(monster_under_attack, str):
                    time_for_fight = float(monster_under_attack.split('_', maxsplit=2)[2][2:])
                    experience = float(monster_under_attack.split('_', maxsplit=2)[1][3:])
                elif isinstance(monster_under_attack, list):
                    for mob in monster_under_attack:
                        time_for_fight += float(mob.split('_', maxsplit=2)[2][2:])
                        experience += float(mob.split('_', maxsplit=2)[1][3:])
                print(f'Вы провели успешную атаку! Потрачено {time_for_fight} секунд, получено {experience} опыта')
                current_experience += experience
                remaining_time -= time_for_fight
                print(f'У вас осталось времени {remaining_time}, всего опыта {current_experience}')
                location_content.pop(user_try_attack)
                answer_is_correct = True

        time.sleep(1)
        print('-' * 60)
        continue

    elif user_action == '2':
        answer_is_correct = False
        while not answer_is_correct:
            print('Вы решили пойти дальше! Выберете локацию!')
            num_of_loc = -1
            for location in location_content:
                # TODO Баг: по аналогии с num_of_monster, num_of_loc некорректно работает, если перед локой есть монстр
                num_of_loc += 1
                if isinstance(location, dict):
                    print(f'{num_of_loc + 1} - {list(location.keys())[0]}')

            user_try_go = input()
            try:
                user_try_go = int(user_try_go)
            except ValueError:
                print('Некорректный ввод')
                time.sleep(1)
                continue
            print(f'Диапазон проверки на стену [0, {num_of_loc}]')
            user_try_go -= 1
            if user_try_go not in [0, num_of_loc]:
                print('Это стена!')
            else:
                next_loc = location_content[user_try_go]
                print('Некс лок', next_loc)
                next_loc_name = list(next_loc.keys())[0]
                # TODO здесь "индексы" user_try_go не совпадают с исходным листом
                answer_is_correct = True

    if next_loc_exist:
        # user_choise = list(tree_of_options['loc_entrance'].keys())[0]  # заглушка - добавить ручной ввод выбора
        user_choise = next_loc_name
        print('Имя новой локации:', user_choise)
        loc_num_in_list = tree_of_options[user_choise]
        print('В листе имеет индекс:', end='')
        print(loc_num_in_list)
        current_location = location_content[loc_num_in_list]  # получение словаря-локации следующего хода
        current_location_name = list(current_location.keys())[0]
        print('-' * 60)

# with open("rpg2.json", "w") as write_file:
#     json.dump(rpg_data, write_file, indent=2)  # dump - запись в переменную
#     # print('Полученный объект', type(rpg_data), 'преобразован в json')

