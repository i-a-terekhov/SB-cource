#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка


import simple_draw as sd
import random


resolution = sd.resolution


def generate_snowflakes(number_of_it):
    color = [
        ['white', sd.COLOR_WHITE],
        ['red', sd.COLOR_RED],
        ['black', sd.COLOR_BLACK],
        ['orange', sd.COLOR_ORANGE],
        ['yellow', sd.COLOR_YELLOW],
        ['blue', sd.COLOR_BLUE],
        ['cyan', sd.COLOR_CYAN],
    ]
    # TODO привести диапазон i к человеческому с 1 до 7
    for i in range(len(color)):
        print(i, '-', color[i][0])
    while True:
        input_volume = input('Выберете цвет снежинок ')
        try:
            input_volume = int(input_volume)
        except ValueError:
            print('Введено некорректное значение типа')
            continue
        if len(color) > input_volume > -1:
            break
        else:
            print('Введено некорректное значение количества')
            continue

    snowflakes = [{
        'Ox': round(random.random() * resolution[0]),
        'Oy': round(resolution[1] * 0.5 + random.random() * resolution[1] * 0.5),
        'length': round(20 + random.random() * 5),
        'color': color[input_volume][1],
        'factor_a': round(0.4 + random.random() * 0.1, 1),
        'factor_b': round(0.4 + random.random() * 0.1, 1),
        'factor_c': round(35 + random.random() * 10),
    } for _ in range(number_of_it)]

    for i in range(len(snowflakes)):
        print(snowflakes[i])
    return snowflakes


def draw_color_snowflakes(snowflakes, current_color=None):
    if current_color is None:
        current_color = snowflakes[0]['color']

    sd.start_drawing()
    for flake in range(len(snowflakes)):
        sd.snowflake(
            center=sd.get_point(snowflakes[flake]['Ox'], snowflakes[flake]['Oy']),
            length=snowflakes[flake]['length'],
            color=current_color,
            factor_a=snowflakes[flake]['factor_a'],
            factor_b=snowflakes[flake]['factor_b'],
            factor_c=snowflakes[flake]['factor_c'],
        )
    sd.finish_drawing()
    sd.sleep(0.1)


def step_down_snowflakes(snowflakes):
    draw_color_snowflakes(snowflakes, current_color=sd.background_color)
    for flake in range(len(snowflakes)):
        snowflakes[flake]['Oy'] -= int(random.random() * 5)
        snowflakes[flake]['Ox'] -= int(random.random() * -6 + 3)
    draw_color_snowflakes(snowflakes, current_color=None)


snow = generate_snowflakes(20)
for i in range(100):
    step_down_snowflakes(snow)


#
# total_frames = 0
# while True:
#     total_frames += 1
#
#     sd.start_drawing()
#     for flake in range(len(snowflakes_dict)):
#
#         if snowflakes_dict[flake]['Oy'] < round(total_frames / 100):
#             snowflakes_dict[flake] = generate_snowflakes(1)[0]
#             print(round(total_frames / 100), snowflakes_dict[flake])
#             continue
#
#         # рисуем снежинки цветом фона
#         sd.snowflake(
#             center=sd.get_point(snowflakes_dict[flake]['Ox'], snowflakes_dict[flake]['Oy']),
#             length=snowflakes_dict[flake]['length'],
#             color=sd.background_color,
#             factor_a=snowflakes_dict[flake]['factor_a'],
#             factor_b=snowflakes_dict[flake]['factor_b'],
#             factor_c=snowflakes_dict[flake]['factor_c'],
#         )
#
#         # считаем координаты следующего местоположения снежинок
#         snowflakes_dict[flake]['Oy'] -= int(random.random() * 5)
#         if round((total_frames / 50)) % 2 == 0:
#             snowflakes_dict[flake]['Ox'] += int(random.random() * 6)
#         elif round((total_frames / 50)) % 2 != 0:
#             snowflakes_dict[flake]['Ox'] -= int(random.random() * 6)
#
#         # рисуем снежинки белым цветом
#         sd.snowflake(
#             center=sd.get_point(snowflakes_dict[flake]['Ox'], snowflakes_dict[flake]['Oy']),
#             length=snowflakes_dict[flake]['length'],
#             color=sd.COLOR_WHITE,
#             factor_a=snowflakes_dict[flake]['factor_a'],
#             factor_b=snowflakes_dict[flake]['factor_b'],
#             factor_c=snowflakes_dict[flake]['factor_c'],
#         )
#
#     sd.finish_drawing()
#     sd.sleep(0.005)
#     if sd.user_want_exit():
#         break
#
# sd.pause()