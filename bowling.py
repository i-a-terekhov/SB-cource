from random import randint


def add_mistakes(game_result):
    def wrap(*args, **kwargs):

        maybe_symbols = "XXX///---000123456789ABCDIFG"
        game_results = game_result(*args, **kwargs)
        replace_count = 0
        for game_number in range(len(game_results)):
            if randint(1, 100) > 90:
                replace_count += 1
                old_game = game_results[game_number]
                old_char = randint(0, len(old_game) - 1)
                new_char = randint(0, len(maybe_symbols) - 1)
                new_game = old_game[:old_char] + maybe_symbols[new_char] + old_game[old_char + 1:]
                game_results[game_number] = new_game
        print(f"Всего испорчено {replace_count} игр")
        return game_results
    return wrap


@add_mistakes
def game_result_generator():
    skittles = 10
    game_results = []

    for game_no in range(10000):
        frames_in_game = 10 if randint(1, 100) > 10 else randint(6, 9)
        game_result = ''

        for frame in range(1, frames_in_game + 1):
            skittles_left = skittles
            frame_result = ""

            for ball_toss in range(1, 3):
                knock_down_skittles = randint(0, skittles_left)
                skittles_left -= knock_down_skittles

                if ball_toss == 1 and skittles_left == 0:
                    frame_result += "X"
                    break
                elif skittles_left == 0:
                    frame_result += "/"
                elif knock_down_skittles == 0:
                    frame_result += "-"
                else:
                    frame_result += str(knock_down_skittles)
            game_result += frame_result
        game_results.append(game_result)
    return game_results


# TODO 1. написать обработчик результатов
# некорректные данные должны вызывать исключения
# «Х» – 20 очков, «4/» - 15 очков, «34» – сумма 3+4=7

def get_score(game_result):
    for game_number in range(len(game_result)):
        game_frames = []

        frame = []
        toss = 1
        for char in game_result[game_number]:
            # if char not in "X-/123456789":
            #     # raise Exception(f"Некорректный символ {char} в {game_result[game_number]}")
            #     print(f"АНОМАЛИЯ ---{game_result[game_number]}-----------------------------------------------------")
            #     # pass
            if char == "X":
                game_frames.append("X")
            else:
                if toss == 1:
                    frame.append(char)
                    toss += 1
                else:
                    toss = 1
                    frame.append(char)
                    game_frames.append(frame)
                    frame = []
        print(f"Игра {game_result[game_number]} --> {game_frames}")
    print()





list_of_result = game_result_generator()
get_score(game_result=list_of_result)
