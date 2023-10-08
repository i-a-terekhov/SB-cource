# (цикл for)
import simple_draw as sd

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for

brick_len = 70
brick_hei = 30

point_x0 = 2
point_y0 = 2 + brick_hei
global_point_x = point_x0
for k in range(12):
    for j in range(6):
        direct_len = [1, 1, 0, 0]
        direct_hei = [0, -1, -1, 0]
        start_point_for_brick = sd.get_point(point_x0, point_y0)
        for i in range(4):
            end_point_for_brick = sd.get_point(point_x0 + brick_len * direct_len[i], point_y0 + brick_hei * direct_hei[i])
            sd.line(start_point=start_point_for_brick, end_point=end_point_for_brick, color=sd.COLOR_DARK_RED, width=5)
            start_point_for_brick = end_point_for_brick
        point_x0 += brick_len
    point_y0 += brick_hei
    point_x0 = global_point_x + (brick_len / 2) * ((k + 1) % 2)
sd.pause()
