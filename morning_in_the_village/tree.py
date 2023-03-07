import random
import simple_draw as sd

if __name__ == '__main__':
    print('Это сообщение распечатается, если модуль вызовут как сценарий')
else:
    print('Импорт модуля...', __name__)


def draw_tree(start_point=sd.get_point(600, 0), angle=90, length=80, width=10):
    deviation = 30
    sd.start_drawing()
    if length < 10:
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
        draw_tree(start_point=branch.end_point, angle=new_angle, length=new_length, width=new_width)
    sd.finish_drawing()
