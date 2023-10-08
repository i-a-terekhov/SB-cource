from pprint import pprint

# Есть словарь координат городов

cites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}

# Составим словарь словарей расстояний между ними
# расстояние на координатной сетке - корень из (x1 - x2) ** 2 + (y1 - y2) ** 2

distances = {}

def distances_calc(a_tuple, b_tuple):
    exact_distance = ((a_tuple[0] - b_tuple[0]) ** 2 + (a_tuple[1] - b_tuple[1]) ** 2) ** 0.5
    return round(exact_distance, 1)

distances['Moscow'], distances['London'], distances['Paris'] = {}, {}, {}
distances['Moscow']['London'] = distances_calc(cites['Moscow'], cites['London'])
distances['Moscow']['Paris'] = distances_calc(cites['Moscow'], cites['Paris'])
distances['London']['Moscow'] = distances_calc(cites['London'], cites['Moscow'])
distances['London']['Paris'] = distances_calc(cites['London'], cites['Paris'])
distances['Paris']['Moscow'] = distances_calc(cites['Paris'], cites['Moscow'])
distances['Paris']['London'] = distances_calc(cites['Paris'], cites['London'])

pprint(distances)




