# нарисовать треугольник из точки (300, 300) с длиной стороны 200
# определить функцию рисования треугольника из заданной точки с заданным наклоном
import simple_draw as sd


def figure(point, angle=0, length=200, width=3):
    quan_corners = 3
    local_point = point
    for i in range(quan_corners):
        side = sd.get_vector(
            start_point=local_point,
            angle=angle + i * (360 / quan_corners),
            length=length,
            width=width
        )
        side.draw()
        local_point = side.end_point


for angl in range(0, 361, 15):
    start_point = sd.get_point(50 + angl, 50 + angl)
    figure(point=start_point, angle=angl, length=100, width=1)

sd.pause()

