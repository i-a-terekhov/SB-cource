# 1) Написать функцию draw_branches, которая должна рисовать две ветви дерева из начальной точки
# Функция должна принимать параметры:
# - точка начала рисования,
# - угол рисования,
# - длина ветвей,
# Отклонение ветвей от угла рисования принять 30 градусов,
import random
import time

# 2) Сделать draw_branches рекурсивной
# - добавить проверку на длину ветвей, если длина меньше 10 - не рисовать
# - вызывать саму себя 2 раза из точек-концов нарисованных ветвей,
#   с параметром "угол рисования" равным углу только что нарисованной ветви,
#   и параметром "длинна ветвей" в 0.75 меньшей чем длина только что нарисованной ветви

# 3) первоначальный вызов:
# root_point = get_point(300, 30)
# draw_bunches(start_point=root_point, angle=90, length=100)

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# Возможный результат решения см lesson_004/results/exercise_04_fractal_01.jpg

# можно поиграть -шрифтами- цветами и углами отклонения

# TODO здесь ваш код

import simple_draw as sd


def draw_branches(start_point, angle, length, width):
    deviation = 30
    if length < 10:
        # time.sleep(0.01)
        sd.circle(center_position=start_point, radius=3, color=sd.COLOR_PURPLE, width=2)
        return None
    for angle in [angle - deviation, angle + deviation]:
        branch = sd.get_vector(start_point=start_point, angle=angle, length=length, width=width)
        branch.draw(color=sd.COLOR_BLACK)
        new_angle = int(angle + deviation * (random.random() * 0.8 - 0.4))
        new_length = int(length * 0.75 + 0.75 * (random.random() * 0.4 - 0.2))
        new_width = int(width * 0.75)
        if new_width < 1:
            new_width = 1
            sd.circle(center_position=branch.end_point, radius=3, color=sd.COLOR_DARK_GREEN, width=3)
        draw_branches(start_point=branch.end_point, angle=new_angle, length=new_length, width=new_width)


# 4) Усложненное задание (делать по желанию)
# - сделать рандомное отклонение угла ветвей в пределах 40% от 30-ти градусов
# - сделать рандомное отклонение длины ветвей в пределах 20% от коэффициента 0.75
# Возможный результат решения см lesson_004/results/exercise_04_fractal_02.jpg

# Пригодятся функции
# sd.random_number()


sd.resolution = (1200, 800)
draw_branches(start_point=sd.get_point(600, 0), angle=90, length=180, width=10)

sd.pause()


