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
from datetime import datetime
import re
import csv

with open("rpg.json", "r") as rpg_file:
    rpg_data = json.load(rpg_file)
    # print('Полученный json преобразован в объект', type(rpg_data))  # <class 'dict'>

# rpg_dumps = json.dumps(rpg_data)  # dumps - запись в переменную в виде строки <- памятка
# print(type(rpg_dumps))


def time_cost(text_name: str):
    pattern = r'tm(\d+)'
    match = re.search(pattern, text_name)
    if match:
        return int(match.group(1))
    else:
        return 0


def exp_calc(text_name: str):
    pattern = r'exp(\d+)'
    match = re.search(pattern, text_name)
    if match:
        return int(match.group(1))
    else:
        return 0


def print_locations_content(location_name: str, entities: list):
    global monster_exist, next_loc_exist, data_of_round
    output_string = f'Вы находитесь в {location_name}. Внутри вы видите:'
    print(output_string)
    data_of_round.append(output_string)
    if monster_exist:
        for ent in entities:
            if ent.get('class') == 'monster':
                output_string = ent.get('representation')
                print(output_string)
                data_of_round.append(output_string)
    if next_loc_exist:
        for ent in entities:
            if ent.get('class') == 'entrance':
                output_string = ent.get('representation')
                print(output_string)
                data_of_round.append(output_string)


def get_correct_input():
    global monster_exist, next_loc_exist, game_over, data_of_round
    while True:
        print('Выберите действие:')
        data_of_round.append('Выберите действие:')
        if monster_exist:
            print('1. Атаковать монстра')
            data_of_round.append('1. Атаковать монстра')
        if next_loc_exist:
            print('2. Перейти в другую локацию')
            data_of_round.append('2. Перейти в другую локацию')
        print('3. Выход')
        data_of_round.append('3. Выход')

        user_input = input()
        data_of_round.append(user_input)
        if user_input == '1' and monster_exist:
            break
        elif user_input == '2' and next_loc_exist:
            break
        elif user_input == '3':
            print('Вы решили завершить игру')
            data_of_round.append('Вы решили завершить игру')
            game_over = True
            break
        else:
            print('Некорректный ввод')
            data_of_round.append('Некорректный ввод')
    return user_input


def user_action_handler(entityes, class_of_entity):
    global data_of_round
    while True:
        output_string = ''
        if class_of_entity == 'monster':
            output_string = 'Вы решили атаковать! Выберете цель!'
        elif class_of_entity == 'entrance':
            output_string = 'Вы решили пойти дальше! Выберете локацию!'

        print(output_string)
        data_of_round.append(output_string)

        num_of_entity = 0
        current_loc_address = {}

        for entity in entityes:
            if entity.get('class') == class_of_entity:
                num_of_entity += 1
                current_loc_address[str(num_of_entity)] = entity.get('address')
                nm = entity['name']
                output_string = f'{num_of_entity} - {nm}'
                print(output_string)
                data_of_round.append(output_string)
        user_try_move = input()
        data_of_round.append(user_try_move)
        if user_try_move not in list(current_loc_address.keys()):
            print('Некорректный ввод')
            data_of_round.append('Некорректный ввод')
        else:
            return entityes[current_loc_address[user_try_move]]


def print_result_of_step(direction, class_of_entity):
    global remaining_time, current_experience, data_of_round

    time_per_move = direction['time']
    experience_for_fight = direction['exp']
    nm = direction['name']
    output_string = ''
    if class_of_entity == 'entrance':
        output_string = f'Вы выбрали новую локацию {nm}!'
    elif class_of_entity == 'monster':
        output_string = f'Вы провели успешную атаку! Потрачено {time_per_move} секунд, получено {experience_for_fight} опыта'
    print(output_string)
    data_of_round.append(output_string)

    remaining_time = float(remaining_time)
    remaining_time -= time_per_move
    current_experience += experience_for_fight

    output_string = f'У вас осталось времени {remaining_time}, всего опыта {current_experience}'
    print(output_string)
    data_of_round.append(output_string)


current_location = rpg_data
current_location_name = list(current_location.keys())[0]
remaining_time = '1234567890.0987654321'
current_experience = 0
game_over = False
game_win = False
time_of_start = datetime.now()
formatted_time = time_of_start.strftime("%Y-%m-%d %H:%M:%S")
print(f'Игра начата в {formatted_time}')
data_of_game = []

while not game_over:
    location_content = current_location[current_location_name]
    list_of_entity = []
    monster_exist = False
    next_loc_exist = False
    for num, entity in enumerate(location_content):
        if isinstance(entity, str):
            monster_exist = True
            name = entity
            rep = '-- Монстра '
            cl = 'monster'
            action_time = time_cost(entity)
            exp = exp_calc(name)
        elif isinstance(entity, list):
            monster_exist = True
            name = ', '.join(entity)
            rep = '-- Группу монстров: '
            cl = 'monster'
            action_time = 0
            exp = 0
            for _ in entity:
                action_time += time_cost(_)
                exp += exp_calc(_)
        else:
            next_loc_exist = True
            name = list(entity.keys())[0]
            rep = '-- Вход в локацию: '
            cl = 'entrance'
            action_time = time_cost(name)
            exp = exp_calc(name)
        list_of_entity.append(({'name': name, 'representation': rep + name, 'class': cl, 'time': action_time, 'exp': exp, 'address': num}))

    data_of_round = []
    time_of_current_moment = datetime.now() - time_of_start
    time_of_current_moment = time_of_current_moment.seconds
    data_of_round.extend([
        f'Вы находитесь в локации {current_location_name}',
        f'У вас {current_experience} опыта и осталось {remaining_time} секунд',
        f'Прошло уже {time_of_current_moment} секунд',
        f'Внутри вы видите:',
    ])

    print_locations_content(current_location_name, list_of_entity)

    user_action = get_correct_input()

    if user_action == '1':
        direction_dict = user_action_handler(list_of_entity, 'monster')
        print_result_of_step(direction_dict, 'monster')
        location_content.pop(direction_dict['address'])
        print('=' * 100)

    elif user_action == '2':
        direction_dict = user_action_handler(list_of_entity, 'entrance')
        print_result_of_step(direction_dict, 'entrance')
        current_location = location_content[direction_dict['address']]
        current_location_name = list(current_location.keys())[0]
        print('=' * 100)

    if current_experience >= 280 and float(remaining_time) >= 0.0:
        print('Вы - победили')
        data_of_round.append('Вы - победили')
        game_over = True
    elif float(remaining_time) < 0.0:
        print('Вы проиграли')
        data_of_round.append('Вы проиграли')
        game_over = True

    data_of_game.append(data_of_round)

with open("dungeon.csv", "a", newline='') as log_file:
    csv_writer = csv.writer(log_file)
    csv_writer.writerows(data_of_game)

# with open("rpg2.json", "w") as write_file:
#     json.dump(rpg_data, write_file, indent=2)  # dump - запись в переменную
#     # print('Полученный объект', type(rpg_data), 'преобразован в json')

