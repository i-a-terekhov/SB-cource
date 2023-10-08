# Есть строка с перечислением фильмов

my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'

# Выведите на консоль с помощью индексации строки, последовательно:
#   первый фильм
#   последний
#   второй
#   второй с конца

# Переопределять my_favorite_movies и использовать .split() нельзя.
# Запятая не должна выводиться.

first_comma = my_favorite_movies.find(',')
second_comma = my_favorite_movies.find(',', first_comma + 1)
first_comma_in_revstr = my_favorite_movies[::-1].find(',') + 1
last_comma = len(my_favorite_movies) - first_comma_in_revstr
penultimate_comma = len(my_favorite_movies) - 1 - my_favorite_movies[::-1].find(',', first_comma_in_revstr)

print(my_favorite_movies[:first_comma])
print(my_favorite_movies[last_comma + 2:])
print(my_favorite_movies[first_comma + 2:second_comma])
print(my_favorite_movies[penultimate_comma + 2:last_comma])
