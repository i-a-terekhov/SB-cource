import unittest
import bowling


class TestBowling(unittest.TestCase):
    # нужно отнаследоваться от этого класса, что бы заработала магия тестирования

    # проверяющие методы должны начинаться с test_
    def test_normal(self):
        # запускаем тестируемую функцию
        result = bowling.get_score(game_result='XXXXXXXXXX')
        # проверяем что она вернула
        self.assertEqual(result, 201)

    # # в именах методов-проверок очень желательно указывать
    # # какой вариант они проверяют
    # def test_sorted(self):
    #     result = my_sort([3, 4, 5])
    #     # так же можно писать детализирующее сообщение
    #     self.assertEqual(result, [3, 4, 5], 'не работает сортировка отсортированного списка')
    #
    # # и так далее - записываем все возможные случаи
    # def test_reversed(self):
    #     result = my_sort([3, 2, 1])
    #     self.assertEqual(result, [1, 2, 3])
    #
    # def test_empty(self):
    #     result = my_sort([])
    #     self.assertEqual(result, [])
    #
    # def test_with_negative(self):
    #     result = my_sort([9, 3, -7, 2])
    #     self.assertEqual(result, [-7, 2, 3, 9])


if __name__ == '__main__':
    # запускам автодискавер тестов
    unittest.main()