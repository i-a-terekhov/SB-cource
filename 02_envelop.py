# (if/elif/else)

# Заданы размеры envelop_x, envelop_y - размеры конверта и paper_x, paper_y листа бумаги
#
# Определить, поместится ли бумага в конверте (стороны листа параллельны сторонам конверта)
#
# Результат проверки вывести на консоль (ДА/НЕТ)
# Использовать только операторы if/elif/else, можно вложенные

envelop_x, envelop_y = 10, 7
paper_book = [
    (8, 9),
    (9, 8),
    (6, 8),
    (8, 6),
    (3, 4),
    (11, 9),
    (9, 11),
]
for paper in paper_book:
    paper_x, paper_y = paper
    answer = ''
    if envelop_x >= paper_x and envelop_y >= paper_y:
        answer = 'ДА'
    else:
        answer = 'НЕТ'
    print(f'Поместится ли в конверте [{envelop_x}, {envelop_y}] лист бумаги [{paper_x}, {paper_y}]?', answer)


# Усложненное задание, решать по желанию.
# Заданы размеры hole_x, hole_y прямоугольного отверстия и размеры brick_х, brick_у, brick_z кирпича (все размеры
# могут быть в диапазоне от 1 до 1000)
#
# Определить, пройдет ли кирпич через отверстие (грани кирпича параллельны сторонам отверстия)

hole_x, hole_y = 8, 9
brick_car = [
    (11, 10, 2),
    (11, 2, 10),
    (10, 11, 2),
    (10, 2, 11),
    (2, 10, 11),
    (2, 11, 10),
    (3, 5, 6),
    (3, 6, 5),
    (6, 3, 5),
    (6, 5, 3),
    (5, 6, 3),
    (5, 3, 6),
    (11, 3, 6),
    (11, 6, 3),
    (6, 11, 3),
    (6, 3, 11),
    (3, 6, 11),
    (3, 11, 6),
]
for brick in brick_car:
    brick_x, brick_y, brick_z = brick
    answer = ''
    if hole_x >= brick_x and hole_y >= brick_y:
        answer = 'ДА'
    else:
        answer = 'НЕТ'
    print(f'Поместится ли в дыре [{hole_x}, {hole_y}] кирпич [{brick_x}, {brick_y}, {brick_z}]?', answer)
