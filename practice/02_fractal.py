# нарисовать ветку дерева из точки (300, 5) вертикально вверх длиной 100
# сделать функцию рисования ветки из заданной точки,
# заданной длины, с заданным наклоном
# написать цикл рисования ветвей с постоянным уменьшением длины на 25% и отклонением на 30 градусов
# сделать функцию branch рекурсивной
import simple_draw as sd

sd.resolution = (600, 800)
point_0 = sd.get_point(300, 5)


def branch(point, angle, length, delta):
    if length < 10:
        return
    mother_branch = sd.get_vector(start_point=point, angle=angle, length=length, width=2)
    mother_branch.draw()
    next_point = mother_branch.end_point
    next_angle = angle - delta
    next_length = length * .75
    branch(point=next_point, angle=next_angle, length=next_length, delta=delta)


for delt in range(-50, 51, 2):
    branch(point=point_0, angle=90, length=(150 - abs(delt)), delta=delt)


sd.pause()

