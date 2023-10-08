import unittest
import random
import bowling


class TestBowling(unittest.TestCase):
    # нужно отнаследоваться от этого класса, что бы заработала магия тестирования

    # проверяющие методы должны начинаться с test_
    def test_1_normal(self):
        print('-' * 20, 'test_1_normal', '-' * 20)
        symbols = '-0123456789'
        for i in range(1000):
            game = ''
            points = 0

            for j in range(10):
                if random.randint(1, 100) > 95:
                    game += 'X'
                    points += 20
                    continue

                frame = ''
                symb = symbols[random.randint(0, len(symbols) - 1)]
                frame += symb
                if symb == '-':
                    symb = '0'
                points += int(symb)

                if random.randint(1, 10) > 9:
                    frame += '/'
                    points += 15 - int(symb)
                else:
                    symb = symbols[random.randint(0, len(symbols) - 1 - int(symb))]
                    frame += symb
                    if symb == '-':
                        symb = '0'
                    points += int(symb)

                game += frame

            result = bowling.get_score(game_result=game)
            print(f'Получили запись {game}, соответсвующую {points} очкам')
            self.assertEqual(result, points, 'проблема в калькуляции при правильной записи игры')

    def test_2_synthetic(self):
        print('-' * 20, 'test_2_synthetic', '-' * 20)
        games = {
            'XXXXXXXXXX': 200,
            '--------------------': 0,
            '11111111111111111111': 20,
            '22222222222222222222': 40,
            '-/-/-/-/-/-/-/-/-/-/': 150,
            '55555555555555555555': 100,
        }
        for game, points in games.items():
            result = bowling.get_score(game_result=game)
            print(f'Получили запись {game}, соответсвующую {points} очкам')
            self.assertEqual(result, points, 'проблема в калькуляции при синтетической записи игры')

    def test_3_more_points_for_game(self):
        print('-' * 20, 'test_3_more_points_for_game', '-' * 20)
        games = {
            'XXXXXXXXXXXXXXXX': None,
            '---------------': None,
            '1111111111111111111111': None,
            '22222222222222222222222': None,
        }
        for game, points in games.items():
            result = bowling.get_score(game_result=game)
            print(f'Получили запись {game}, соответсвующую {points} очкам')
            self.assertEqual(result, points, 'некорректные входные данные не были выявлены тестируемой функцией')

    def test_4_more_points_for_frame(self):
        print('-' * 20, 'test_4_more_points_for_frame', '-' * 20)
        games = {
            '99999999999999999999': None,
            '22222222222222222222222': None,
        }
        for game, points in games.items():
            result = bowling.get_score(game_result=game)
            print(f'Получили запись {game}, соответсвующую {points} очкам')
            self.assertEqual(result, points, 'избыток очков во фрейме не был выявлен тестируемой функцией')


if __name__ == '__main__':
    # запускам автодискавер тестов
    unittest.main()
