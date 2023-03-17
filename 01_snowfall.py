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


flake = Snowflake()

while True:
    flake.clear_previous_picture()
    flake.move()
    flake.draw()
    if not flake.can_fall():
        break
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:
# flakes = get_flakes(count=N)  # создать список снежинок
# while True:
#     for flake in flakes:
#         flake.clear_previous_picture()
#         flake.move()
#         flake.draw()
#     fallen_flakes = get_fallen_flakes()  # подчитать сколько снежинок уже упало
#     if fallen_flakes:
#         append_flakes(count=fallen_flakes)  # добавить еще сверху
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break

sd.pause()
