# (определение функций)
import simple_draw as sd
import random

# Написать функцию отрисовки смайлика в произвольной точке экрана
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.

def give_smile(point_x0=100, point_y0=100, size=100):
    color = sd.random_color()
    central_point = sd.get_point(point_x0, point_y0)
    sd.circle(center_position=central_point, radius=size, width=int(size * 0.03), color=color)
    height_of_smile = size / 4
    smile_list = [
        sd.get_point(point_x0 - int(size / 1.7), point_y0 - int(size / 9 + height_of_smile)),
        sd.get_point(point_x0 - int(size / 2), point_y0 - int(size / 8 + height_of_smile)),
        sd.get_point(point_x0 - int(size / 4), point_y0 - int(size / 4 + height_of_smile)),
        sd.get_point(point_x0, point_y0 - int(size / 3.5 + height_of_smile)),
        sd.get_point(point_x0 + int(size / 4), point_y0 - int(size / 4 + height_of_smile)),
        sd.get_point(point_x0 + int(size / 2), point_y0 - int(size / 8 + height_of_smile)),
        sd.get_point(point_x0 + int(size / 1.7), point_y0 - int(size / 9 + height_of_smile)),
    ]
    sd.lines(point_list=smile_list, width=int(size * 0.03), color=color)
    for i in (-1, 1):
        point_of_eye = sd.get_point(point_x0 + (size / 3) * i, point_y0 + size / 4)
        sd.circle(center_position=point_of_eye, radius=int(size / 6), width=int(size * 0.03), color=color)

for i in range(1150):
    x = int(random.random() * 550)
    y = int(random.random() * 550)
    r = int(random.random() * 200)
    give_smile(x, y, r)

sd.pause()