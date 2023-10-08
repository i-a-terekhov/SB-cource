# -*- coding: utf-8 -*-

import simple_draw as sd

# На основе вашего кода из решения lesson_004/01_shapes.py сделать функцию-фабрику,
# которая возвращает функции рисования треугольника, четырехугольника, пятиугольника и т.д.
#
# Функция рисования должна принимать параметры
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Функция-фабрика должна принимать параметр n - количество сторон.


def get_polygon(n):
    number_of_sides = n

    def get_figure(point=(10, 10), angle=0, length=200):
        start_point = sd.get_point(point[0], point[1])
        for i in range(number_of_sides):
            side = sd.get_vector(
                start_point=start_point,
                angle=angle + (360 / number_of_sides) * i,
                length=length,
                width=3)
            side.draw()
            start_point = side.end_point
    return get_figure


draw_triangle = get_polygon(n=3)
draw_triangle()
draw_triangle(point=(200, 200), angle=13, length=100)

draw_ugly_angel = get_polygon(100)
draw_ugly_angel(point=(250, 150), length=2)

sd.pause()
