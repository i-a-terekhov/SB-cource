import simple_draw as sd

if __name__ == '__main__':
    print('Это сообщение распечатается, если модуль вызовут как сценарий')
else:
    print('Импорт модуля...', __name__)


def draw_rainbow():
    colors = [
        sd.COLOR_RED,
        sd.COLOR_ORANGE,
        sd.COLOR_YELLOW,
        sd.COLOR_GREEN,
        sd.COLOR_CYAN,
        sd.COLOR_BLUE,
        sd.COLOR_PURPLE,
    ]
    dark_colors = [
        sd.COLOR_DARK_RED,
        sd.COLOR_DARK_ORANGE,
        sd.COLOR_DARK_YELLOW,
        sd.COLOR_DARK_GREEN,
        sd.COLOR_DARK_CYAN,
        sd.COLOR_DARK_BLUE,
        sd.COLOR_DARK_PURPLE,
    ]

    resolution = sd.resolution
    radius = int(resolution[0] * 1.2)
    thickness = int(resolution[0] / 80)
    point_x = - int(resolution[0] * 0.2)
    point_y = - int(resolution[1] * 0.8)
    rainbow_centre = sd.get_point(point_x, point_y)

    second_per_line = 0.01
    base_time_limit = 0.3
    while second_per_line < base_time_limit:
        second_per_line += 0.1

        for current_line_index in range(len(colors)):
            sd.circle(
                center_position=rainbow_centre,
                radius=radius + current_line_index * thickness,
                color=colors[current_line_index],
                width=thickness
            )
            if second_per_line < base_time_limit * 0.92:
                light_rainbow_lines = 4
                last_line_index = colors.index(colors[current_line_index - light_rainbow_lines])
                sd.circle(
                    center_position=rainbow_centre,
                    radius=radius + last_line_index * thickness,
                    color=dark_colors[last_line_index],
                    width=thickness
                )
            sd.sleep(second_per_line)

