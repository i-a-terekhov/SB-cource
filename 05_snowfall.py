# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные

# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()

import simple_draw as sd
import random


def generate_snowflakes(number_of_it):
    snowflakes = [{
        'Ox': round(0 + random.random() * 1200),
        'Oy': round(600 + random.random() * 600),
        'length': round(20 + random.random() * 5),
        'factor_a': round(0.4 + random.random() * 0.1, 1),
        'factor_b': round(0.4 + random.random() * 0.1, 1),
        'factor_c': round(35 + random.random() * 10),
    } for i in range(number_of_it)]
    return snowflakes


sd.resolution = (1200, 600)
snowflakes_dict = generate_snowflakes(40)

total_frames = 0
while True:
    total_frames += 1

    sd.start_drawing()
    for flake in range(len(snowflakes_dict)):

        if snowflakes_dict[flake]['Oy'] < round(total_frames / 100):
            snowflakes_dict[flake] = generate_snowflakes(1)[0]
            print(round(total_frames / 100), snowflakes_dict[flake])
            continue

        # рисуем снежинки цветом фона
        sd.snowflake(
            center=sd.get_point(snowflakes_dict[flake]['Ox'], snowflakes_dict[flake]['Oy']),
            length=snowflakes_dict[flake]['length'],
            color=sd.background_color,
            factor_a=snowflakes_dict[flake]['factor_a'],
            factor_b=snowflakes_dict[flake]['factor_b'],
            factor_c=snowflakes_dict[flake]['factor_c'],
        )

        # считаем координаты следующего местоположения снежинок
        snowflakes_dict[flake]['Oy'] -= int(random.random() * 5)
        if round((total_frames / 50)) % 2 == 0:
            snowflakes_dict[flake]['Ox'] += int(random.random() * 6)
        elif round((total_frames / 50)) % 2 != 0:
            snowflakes_dict[flake]['Ox'] -= int(random.random() * 6)

        # рисуем снежинки белым цветом
        sd.snowflake(
            center=sd.get_point(snowflakes_dict[flake]['Ox'], snowflakes_dict[flake]['Oy']),
            length=snowflakes_dict[flake]['length'],
            color=sd.COLOR_WHITE,
            factor_a=snowflakes_dict[flake]['factor_a'],
            factor_b=snowflakes_dict[flake]['factor_b'],
            factor_c=snowflakes_dict[flake]['factor_c'],
        )

    sd.finish_drawing()
    sd.sleep(0.005)
    if sd.user_want_exit():
        break

sd.pause()

# подсказка! для ускорения отрисовки можно
#  - убрать clear_screen()
#  - в начале рисования всех снежинок вызвать sd.start_drawing()
#  - на старом месте снежинки отрисовать её же, но цветом sd.background_color
#  - сдвинуть снежинку
#  - отрисовать её цветом sd.COLOR_WHITE на новом месте
#  - после отрисовки всех снежинок, перед sleep(), вызвать sd.finish_drawing()


# 4) Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg


