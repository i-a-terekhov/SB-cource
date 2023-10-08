import simple_draw as sd
import random

sd.resolution = (1200, 600)

# реализовать падение одной снежинки
# реализовать падение одной снежинки из произвольного места экрана
# реализовать падение одной снежинки с ветром - смещение в сторону
y = 500
x = 100

while True:
    sd.clear_screen()
    point = sd.get_point(x, y)
    sd.snowflake(center=point, length=150, factor_a=0.5, factor_b=0.3, factor_c=60)
    sd.snowflake(center=point, length=100, factor_a=0.5, factor_b=0.2, factor_c=60)
    y -= 1 + random.random() * 3
    if y < 50:
       break
    x = x + 3 + (-5 + random.random() * 5)

    sd.sleep(0.06)
    if sd.user_want_exit():
        break

sd.pause()
