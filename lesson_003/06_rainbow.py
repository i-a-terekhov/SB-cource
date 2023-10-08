# (цикл for)

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

# Нарисовать радугу: 7 линий разного цвета толщиной 4 с шагом 5 из точки (50, 50) в точку (350, 450)
point_for_circle = sd.get_point(-50, -50)
for i in range(7):
    point_for_line_start = sd.get_point(50 - i * 2.5, 50 + i * 2.5)
    point_for_line_end = sd.get_point(350 - i * 2.5, 450 + i * 2.5)
    sd.circle(center_position=point_for_circle, radius=500+i*15, color=rainbow_colors[i], width=15)
    sd.line(start_point=point_for_line_start, end_point=point_for_line_end, color=rainbow_colors[i], width=4)

# Усложненное задание, делать по желанию.
# Нарисовать радугу дугами от окружности (cсм sd.circle) за нижним краем экрана,
# поэкспериментировать с параметрами, что бы было красиво

sd.pause()
