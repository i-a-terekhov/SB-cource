# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())

class NonKnowElement:
    """Неизвестный элемент"""

    def __str__(self):
        return f'Ничего не произошло, Вам не хватает знания алхимии для превращения'


class Water:
    """Вода"""

    def __str__(self):
        return f'Водне'

    def __add__(self, other):
        if type(other) is Air:
            return Storm()
        elif type(other) is Fire:
            return Vapor()
        elif type(other) is Ground:
            return Dirt()
        else:
            return NonKnowElement()


class Air:
    """Воздух"""

    def __str__(self):
        return f'Воздуше'

    def __add__(self, other):
        if type(other) is Fire:
            return Bolt()
        elif type(other) is Ground:
            return Dust()
        else:
            return NonKnowElement()


class Fire:
    """Огонь"""

    def __str__(self):
        return f'Огне'

    def __add__(self, other):
        if type(other) is Ground:
            return Lava()
        else:
            return NonKnowElement()


class Ground:
    """Земля"""

    def __str__(self):
        return f'Земле'

    def __add__(self, other):
        return NonKnowElement()


class Storm:
    """Шторм"""

    def __str__(self):
        return f'Шторме'

    def __add__(self, other):
        return NonKnowElement()


class Vapor:
    """Пар"""

    def __str__(self):
        return f'Паре'

    def __add__(self, other):
        return NonKnowElement()


class Dirt:
    """Грязь"""

    def __str__(self):
        return f'Грязе'

    def __add__(self, other):
        return NonKnowElement()


class Bolt:
    """Молния"""

    def __str__(self):
        return f'Молние'

    def __add__(self, other):
        return NonKnowElement()


class Dust:
    """Пыль"""

    def __str__(self):
        return f'Пылие'

    def __add__(self, other):
        return NonKnowElement()


class Lava:
    """Лава"""

    def __str__(self):
        return f'Лавие'

    def __add__(self, other):
        return NonKnowElement()


print(Water(), '+', Air(), '=', Water() + Air())
print(Water(), '+', Fire(), '=', Water() + Fire())
print(Water(), '+', Ground(), '=', Water() + Ground())
print(Water(), '+', Dirt(), '=', Water() + Dirt())
print(Air(), '+', Fire(), '=', Air() + Fire())
print(Air(), '+', Ground(), '=', Air() + Ground())
print(Fire(), '+', Ground(), '=', Fire() + Ground())
print(Ground(), '+', Ground(), '=', Ground() + Ground())


# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.
