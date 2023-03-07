# Создать пакет, в который скопировать функции отрисовки из предыдущего урока
#  - радуги
#  - стены
#  - дерева
#  - смайлика
#  - снежинок
# Функции по модулям разместить по тематике. Название пакета и модулей - по смыслу.
# Создать модуль с функцией отрисовки кирпичного дома с широким окном и крышей.

# С помощью созданного пакета нарисовать эпохальное полотно "Утро в деревне".
# На картине должны быть:
#  - кирпичный дом, в окошке - смайлик.
#  - слева от дома - сугроб (предположим что это ранняя весна)
#  - справа от дома - дерево (можно несколько)
#  - справа в небе - радуга, слева - солнце (весна же!)
# пример см. lesson_005/results/04_painting.jpg
# Приправить своей фантазией по вкусу (коты? коровы? люди? трактор? что придумается)


# Усложненное задание (делать по желанию)
# Анимировать картину.
# Пусть слева идет снегопад, радуга переливается цветами, смайлик моргает, солнце крутит лучами, етс.
# Задержку в анимировании все равно надо ставить, пусть даже 0.01 сек - так библиотека устойчивей работает.

import simple_draw as sd
import morning_in_the_village.rainbow as rain
import morning_in_the_village.house as house
import morning_in_the_village.tree as tree
import morning_in_the_village.snowfall as snowfall


sd.resolution = (1200, 800)
sd.background_color = sd.COLOR_CYAN


def nuke_effect():
    colors = [
        sd.COLOR_WHITE, sd.COLOR_YELLOW, sd.COLOR_DARK_YELLOW,
        sd.COLOR_ORANGE, sd.COLOR_DARK_ORANGE,
        sd.COLOR_DARK_RED, sd.COLOR_BLACK
    ]
    first_sleep = 0.2
    base_sleep = first_sleep * len(colors)
    for i in range(len(colors)):
        sd.rectangle(
            left_bottom=sd.get_point(0, 0),
            right_top=sd.get_point(sd.resolution[0], sd.resolution[1]),
            color=colors[i], width=0)
        sd.sleep(base_sleep - first_sleep * i)
    sd.sleep(2)


house.draw_wall()
house.draw_window()
house.draw_roof()
tree.draw_tree()
rain.draw_rainbow()
nuke_effect()
sd.background_color = sd.COLOR_BLACK
snowfall.draw_snowfall()

