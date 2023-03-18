import simple_draw as sd
import random


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:

    def __init__(self):
        self.resolution = sd.resolution
        self.param = {
            'Ox': round(random.random() * self.resolution[0]),
            'Oy': round(self.resolution[1] + random.random() * self.resolution[1] * 0.2),
            'length': round(20 + random.random() * 5),
            'color': None,
            'factor_a': round(0.4 + random.random() * 0.1, 1),
            'factor_b': round(0.4 + random.random() * 0.1, 1),
            'factor_c': round(35 + random.random() * 10),
        }

    def clear_previous_picture(self):
        background_color = sd.background_color
        self.draw(background_color)

    def move(self):
        self.param['Oy'] -= int(random.random() * 15)
        self.param['Ox'] -= int(random.random() * -10 + 5)

    def draw(self, color=None):
        if color is None:
            color = sd.COLOR_WHITE
        sd.snowflake(
            center=sd.get_point(self.param['Ox'], self.param['Oy']),
            length=self.param['length'],
            color=color,
            factor_a=self.param['factor_a'],
            factor_b=self.param['factor_b'],
            factor_c=self.param['factor_c'],
        )

    def can_fall(self):
        if self.param['Oy'] > 10:
            return True
        else:
            return False


def get_flakes(count=20):
    snowflakes = [
        Snowflake() for _ in range(count)
    ]
    return snowflakes


def get_fallen_flakes(snowflakes):
    fallen_flakes = []
    number_of_deletions_in_this_run = 0
    for flake in range(len(snowflakes)):
        if snowflakes[flake - number_of_deletions_in_this_run].param['Oy'] < 1:
            fallen_flakes.append(flake)
            del snowflakes[flake - number_of_deletions_in_this_run]
            number_of_deletions_in_this_run += 1
    return fallen_flakes


def append_flakes(current_flakes=None, needed_flakes=None):
    if current_flakes is None:
        current_flakes = []
    if needed_flakes is None:
        needed_flakes = []
    needed_flakes = len(needed_flakes)
    new_flakes = get_flakes(needed_flakes)
    current_flakes.extend(new_flakes)


# flake = Snowflake()
#
# while True:
#     flake.clear_previous_picture()
#     flake.move()
#     flake.draw()
#     if not flake.can_fall():
#         break
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break

# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:
flakes = get_flakes(count=20)  # создать список снежинок
while True:
    for flake in flakes:
        flake.clear_previous_picture()
        flake.move()
        flake.draw()
    fallen_flakes = get_fallen_flakes(flakes)  # подчитать сколько снежинок уже упало
    if fallen_flakes:
        append_flakes(current_flakes=flakes, needed_flakes=fallen_flakes)  # добавить еще
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
