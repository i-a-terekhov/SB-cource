# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg

import simple_draw as sd


def choose_a_shape():
    shapes = [
        'треугольник',
        'квадрат',
        'пятиугольник',
        'шестиугольник',
    ]
    for i in range(len(shapes)):
        print(i, ':', shapes[i])
    while True:
        print('Выберите фигуру: ', end='')
        answer = input()
        if not answer.isdigit():
            print('Вы ввели не число')
        elif int(answer) not in range(len(shapes)):
            print('Вы ввели число, отсутствующее в списке')
        else:
            break
    answer = int(answer)

    if answer == 0:
        draw_triangle()
    elif answer == 1:
        draw_square()
    elif answer == 2:
        draw_pentagon()
    elif answer == 3:
        draw_hexagon()


def draw_figure(point=(200, 200), angle=0, length=200, color=sd.COLOR_RED, number_of_sides=3):
    start_point = sd.get_point(point[0], point[1])
    for i in range(number_of_sides):
        side = sd.get_vector(start_point=start_point, angle=angle + (360 / number_of_sides) * i, length=length, width=5)
        side.draw(color=color)
        start_point = side.end_point


def draw_triangle(*args, **kwargs):
    draw_figure(*args, **kwargs, number_of_sides=3)


def draw_square(*args, **kwargs):
    draw_figure(*args, **kwargs, number_of_sides=4)


def draw_pentagon(*args, **kwargs):
    draw_figure(*args, **kwargs, number_of_sides=5)


def draw_hexagon(*args, **kwargs):
    draw_figure(*args, **kwargs, number_of_sides=6)


choose_a_shape()

sd.pause()
