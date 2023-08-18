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


def search_exceptions(get_score_function):
    def wrap(game_result):

        new_game_results = []
        for i in game_result:
            try:
                get_scores = get_score_function([i])
                new_game_results.append(get_scores)
            except Exception as e:
                print(f"Исключение: {e}")
        return new_game_results
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


@search_exceptions
def get_score(game_result):
    reformat_game_result = []
    for game in game_result:
        game_frames = []
        frame = []
        toss = 1
        for char in game:
            if char == "X":
                game_frames.append("X")
            else:
                if toss == 1:
                    frame.append(char)
                    toss += 1
                else:
                    frame.append(char)
                    game_frames.append(frame)
                    frame = []
                    toss = 1
        reformat_game_result.append(game_frames)
        # print(f"Игра {game} --> {game_frames} ---> {0} очков")

    for game in reformat_game_result:
        game_score = 0
        if len(game) != 10:
            raise Exception(f"Игра не окончена {game}")
        for frame in game:
            if frame == "X":
                game_score += 20
            else:
                if frame[0] == "-":
                    frame[0] = "0"
                if frame[1] == "-":
                    frame[1] = "0"

                if frame[0] == "/":
                    raise Exception(f"Некорректная запись в игре {game}, во фрейме {frame}")
                elif frame[1] == "/":
                    game_score += 15

                elif frame[0] not in "1234567890" or frame[1] not in "1234567890":
                    raise Exception(f"Некорректный символ в игре {game}, во фрейме {frame}")
                else:
                    game_score += int(frame[0]) + int(frame[1])
        print(f"Игра {game} ---> {game_score} очков")


list_of_result = game_result_generator()
get_score(game_result=list_of_result)
