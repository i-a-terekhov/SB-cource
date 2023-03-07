import random
import simple_draw as sd

if __name__ == '__main__':
    print('Это сообщение распечатается, если модуль вызовут как сценарий')
else:
    print('Импорт модуля...', __name__)


def generate_snowflakes(number_of_it):
    snowflakes = [{
        'Ox': round(0 + random.random() * sd.resolution[0]),
        'Oy': round(sd.resolution[1] + random.random() * sd.resolution[1]),
        'length': round(20 + random.random() * 5),
        'factor_a': round(0.4 + random.random() * 0.1, 1),
        'factor_b': round(0.4 + random.random() * 0.1, 1),
        'factor_c': round(35 + random.random() * 10),
    } for i in range(number_of_it)]
    return snowflakes


def draw_snowfall():
    snowflakes_dict = generate_snowflakes(40)
    total_frames = 0
    while True:
        total_frames += 1

        sd.start_drawing()
        for flake in range(len(snowflakes_dict)):

            if snowflakes_dict[flake]['Oy'] < round(total_frames / 100):
                snowflakes_dict[flake] = generate_snowflakes(1)[0]
                print(round(total_frames / 100), snowflakes_dict[flake])
                continue

            # рисуем снежинки цветом фона
            sd.snowflake(
                center=sd.get_point(snowflakes_dict[flake]['Ox'], snowflakes_dict[flake]['Oy']),
                length=snowflakes_dict[flake]['length'],
                color=sd.background_color,
                factor_a=snowflakes_dict[flake]['factor_a'],
                factor_b=snowflakes_dict[flake]['factor_b'],
                factor_c=snowflakes_dict[flake]['factor_c'],
            )

            # считаем координаты следующего местоположения снежинок
            snowflakes_dict[flake]['Oy'] -= int(random.random() * 5)
            if round((total_frames / 50)) % 2 == 0:
                snowflakes_dict[flake]['Ox'] += int(random.random() * 6)
            elif round((total_frames / 50)) % 2 != 0:
                snowflakes_dict[flake]['Ox'] -= int(random.random() * 6)

            # рисуем снежинки белым цветом
            sd.snowflake(
                center=sd.get_point(snowflakes_dict[flake]['Ox'], snowflakes_dict[flake]['Oy']),
                length=snowflakes_dict[flake]['length'],
                color=sd.COLOR_WHITE,
                factor_a=snowflakes_dict[flake]['factor_a'],
                factor_b=snowflakes_dict[flake]['factor_b'],
                factor_c=snowflakes_dict[flake]['factor_c'],
            )

        sd.finish_drawing()
        sd.sleep(0.005)
        if sd.user_want_exit():
            break
