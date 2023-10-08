# Добавить цвет в функции рисования геом. фигур. из упр lesson_004/01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих:
#   вывести список всех цветов с номерами и ждать ввода номера желаемого цвета.
# Потом нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см lesson_004/results/exercise_02_global_color.jpg

import simple_draw as sd


def choose_a_color():
    colors = [
        ['red', sd.COLOR_RED],
        ['orange', sd.COLOR_ORANGE],
        ['yellow', sd.COLOR_YELLOW],
        ['green', sd.COLOR_GREEN],
        ['cyan', sd.COLOR_CYAN],
        ['blue', sd.COLOR_BLUE],
        ['purple', sd.COLOR_PURPLE],
    ]
    for i in range(len(colors)):
        print(i, ':', colors[i][0])
    while True:
        print('Выберите цвет фигур: ', end='')
        answer = input()
        if not answer.isdigit():
            print('Вы ввели не число')
        elif int(answer) not in range(len(colors)):
            print('Вы ввели число, отсутствующее в списке')
        else:
            break
    answer = int(answer)
    return colors[answer][1]


def draw_figure(point=(10, 10), angle=0, length=200, color=sd.COLOR_RED, number_of_sides=3):
    start_point = sd.get_point(point[0], point[1])
    for i in range(number_of_sides):
        side = sd.get_vector(start_point=start_point, angle=angle + (360 / number_of_sides) * i, length=length, width=5)
        side.draw(color=color)
        start_point = side.end_point


def draw_triange(*args, **kwargs):
    draw_figure(*args, **kwargs, number_of_sides=3)


def draw_square(*args, **kwargs):
    draw_figure(*args, **kwargs, number_of_sides=4)


color = choose_a_color()
draw_triange(point=(250, 250), color=color)
draw_square(color=color)

sd.pause()
