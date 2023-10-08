import simple_draw as sd

if __name__ == '__main__':
    print('Это сообщение распечатается, если модуль вызовут как сценарий')
else:
    print('Импорт модуля...', __name__)


def draw_wall():
    total_rows_in_height = 15
    base_number_of_bricks_in_row = 6

    brick_length = 40
    brick_height = 15
    half_brick_length = brick_length / 2

    point_x0 = 100
    point_y0 = 2 + brick_height
    zero_point_x = point_x0

    start_point_for_wall = sd.get_point(point_x0, point_y0 - total_rows_in_height * brick_height)
    end_point_for_wall = sd.get_point(
        point_x0 + base_number_of_bricks_in_row * brick_length,
        point_y0 * total_rows_in_height - brick_height * 2)
    sd.rectangle(left_bottom=start_point_for_wall, right_top=end_point_for_wall, color=sd.COLOR_RED)

    for row_num in range(total_rows_in_height):
        if row_num % 2 == 0:
            total_bricks_in_row = base_number_of_bricks_in_row + 1
        else:
            total_bricks_in_row = base_number_of_bricks_in_row

        for brick_num in range(total_bricks_in_row):
            if (brick_num == 0 or brick_num == total_bricks_in_row - 1) and row_num % 2 == 0:
                current_brick_len = half_brick_length
            else:
                current_brick_len = brick_length

            horizontal_side_direction = [1, 1, 0, 0]
            vertical_side_direction = [0, -1, -1, 0]
            start_point_for_side = sd.get_point(point_x0, point_y0)
            for side in range(4):
                end_point_for_side = sd.get_point(
                    point_x0 + current_brick_len * horizontal_side_direction[side],
                    point_y0 + brick_height * vertical_side_direction[side]
                )
                sd.line(start_point=start_point_for_side, end_point=end_point_for_side,
                        color=sd.COLOR_DARK_RED, width=3)
                start_point_for_side = end_point_for_side
            point_x0 += current_brick_len

        point_x0 = zero_point_x
        point_y0 += brick_height


def draw_window():
    window_length = 120
    window_height = 100
    vertical_crosspiece = window_length / 2
    horizontal_crosspiece = window_height / 2

    point_x0 = 160
    point_y0 = 160

    horizontal_side_direction = [1, 1, 0, 0]
    vertical_side_direction = [0, -1, -1, 0]

    start_point_for_window = sd.get_point(point_x0, point_y0 - window_height)
    end_point_for_window = sd.get_point(point_x0 + window_length, point_y0)
    sd.rectangle(left_bottom=start_point_for_window, right_top=end_point_for_window, color=sd.COLOR_BLUE)

    start_point_for_side = sd.get_point(point_x0, point_y0)
    for side in range(4):
        end_point_for_side = sd.get_point(
            point_x0 + window_length * horizontal_side_direction[side],
            point_y0 + window_height * vertical_side_direction[side])
        sd.line(start_point=start_point_for_side, end_point=end_point_for_side,
                color=sd.COLOR_WHITE, width=7)
        start_point_for_side = end_point_for_side

    start_point_for_side = sd.get_point(
        point_x0 + vertical_crosspiece, point_y0 - window_height)
    end_point_for_side = sd.get_point(
        point_x0 + vertical_crosspiece, point_y0)
    sd.line(start_point=start_point_for_side, end_point=end_point_for_side,
            color=sd.COLOR_WHITE, width=3)

    start_point_for_side = sd.get_point(
        point_x0, point_y0 - horizontal_crosspiece)
    end_point_for_side = sd.get_point(
        point_x0 + window_length, point_y0 - horizontal_crosspiece)
    sd.line(start_point=start_point_for_side, end_point=end_point_for_side,
            color=sd.COLOR_WHITE, width=3)


def draw_roof():
    point_a = sd.get_point(90, 230)
    point_b = sd.get_point(350, 230)
    point_c = sd.get_point(220, 350)
    sd.polygon(point_list=(point_a, point_b, point_c), color=sd.COLOR_DARK_GREEN, width=0)

