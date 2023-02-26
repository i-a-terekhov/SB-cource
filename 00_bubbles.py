import simple_draw as sd


sd.resolution = (1200, 600)

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
point = sd.get_point(100, 100)
radius = 45
for i in range(3):
    radius += 5
    sd.circle(center_position=point, radius=radius)

# Написать функцию рисования пузырька, принммающую 2 (или более) параметра: точка рисовании и шаг
def buble(radius, point, step, width):
    for i in range(3):
        radius += step
        sd.circle(center_position=point, radius=radius, width=width)

radius = 150
point = sd.get_point(200, 200)
step = 150
width = 1

buble(radius, point, step, width)

# Нарисовать 10 пузырьков в ряд
for i in range(0, 500, 50):
    point = sd.get_point(100 + i, 300)
    sd.circle(center_position=point)

# Нарисовать три ряда по 10 пузырьков
for i in range(0, 150, 50):
    for j in range(0, 500, 50):
        point = sd.get_point(300 + j, 400 + i)
        sd.circle(center_position=point)

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
quant_x = 600
quant_y = 300
for k in range(10000):
    while True:
        pre_quant_x = quant_x + sd.random_number(-30,30)
        if 0 > pre_quant_x or pre_quant_x > 1200:
            continue
        if 585 < pre_quant_x < 615:
            continue
        quant_x = pre_quant_x
        break
    while True:
        pre_quant_y = quant_y + sd.random_number(-30,30)
        if 0 > pre_quant_y or pre_quant_y > 600:
            continue
        if 295 < pre_quant_y < 315:
            continue
        quant_y = pre_quant_y
        break

    point = sd.get_point(quant_x, quant_y)
    radius = sd.random_number(10, 15)
    color = sd.random_color()
    sd.circle(center_position=point, radius=radius, color=color, width=3)

point = sd.get_point(600, 300)
sd.circle(center_position=point, radius=300, width=20)

sd.pause()


