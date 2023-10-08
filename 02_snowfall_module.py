# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall

import simple_draw as sd
import snowfall_engine as engine

sd.resolution = (1200, 300)

color = engine.set_the_color()
snow = engine.generate_snowflakes(20, color=color)

while True:
    engine.step_down_snowflakes(snow)
    fall = engine.get_number_of_fallen_flakes(snow)
    if len(fall) > 0:
        snow.extend(engine.generate_snowflakes(len(fall), color))
        engine.del_fallen_flakes(snow, fall)
    if sd.user_want_exit():
        break
sd.pause()
