#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка


import simple_draw as sd
import random


def set_the_color():
    color = [
        ['white', sd.COLOR_WHITE],
        ['red', sd.COLOR_RED],
        ['black', sd.COLOR_BLACK],
        ['orange', sd.COLOR_ORANGE],
        ['yellow', sd.COLOR_YELLOW],
        ['blue', sd.COLOR_BLUE],
        ['cyan', sd.COLOR_CYAN],
    ]
    for col_num in range(len(color)):
        print(col_num + 1, '-', color[col_num][0])
    while True:
        input_volume = input('Выберете цвет снежинок ')
        try:
            input_volume = int(input_volume) - 1
        except ValueError:
            print('Введено некорректное значение типа')
            continue
        if len(color) > input_volume > -1:
            break
        else:
            print('Введено некорректное значение количества')
            continue
    return color[input_volume][1]


def generate_snowflakes(number_of_it, color=sd.COLOR_WHITE):
    resolution = sd.resolution
    snowflakes = [{
        'Ox': round(random.random() * resolution[0]),
        'Oy': round(resolution[1] + random.random() * resolution[1] * 0.5),
        'length': round(20 + random.random() * 5),
        'color': color,
        'factor_a': round(0.4 + random.random() * 0.1, 1),
        'factor_b': round(0.4 + random.random() * 0.1, 1),
        'factor_c': round(35 + random.random() * 10),
    } for _ in range(number_of_it)]
    return snowflakes


def draw_color_snowflakes(snowflakes, current_color=None):
    if current_color is None:
        current_color = snowflakes[0]['color']

    for flake in range(len(snowflakes)):
        sd.snowflake(
            center=sd.get_point(snowflakes[flake]['Ox'], snowflakes[flake]['Oy']),
            length=snowflakes[flake]['length'],
            color=current_color,
            factor_a=snowflakes[flake]['factor_a'],
            factor_b=snowflakes[flake]['factor_b'],
            factor_c=snowflakes[flake]['factor_c'],
        )


def step_down_snowflakes(snowflakes):
    if len(snowflakes) == 0:
        print('Для снегопада нет ресурсов')
        return None

    sd.start_drawing()
    draw_color_snowflakes(snowflakes, current_color=sd.background_color)
    for flake in range(len(snowflakes)):
        snowflakes[flake]['Oy'] -= int(random.random() * 15)
        snowflakes[flake]['Ox'] -= int(random.random() * -6 + 3)
    draw_color_snowflakes(snowflakes, current_color=None)
    sd.finish_drawing()
    sd.sleep(0.1)


def get_number_of_fallen_flakes(snowflakes):
    fallen_flakes = []
    for flake in range(len(snowflakes)):
        if snowflakes[flake]['Oy'] < 1:
            fallen_flakes.append(flake)
    return fallen_flakes


def del_fallen_flakes(snowflakes, fallen_flakes: list):
    number_of_deletions_in_this_run = 0
    for i in fallen_flakes:
        del snowflakes[i - number_of_deletions_in_this_run]
        number_of_deletions_in_this_run += 1
