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
    def wrap(*args, **kwargs):
        try:
            score = get_score_function(*args, **kwargs)
            return score
        except Exception as e:
            print(f"Исключение: {e}")
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
    game_frames = []
    frame = []
    toss = 1
    for char in game_result:
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

    game_score = 0
    if len(game_frames) != 10:
        raise Exception(f"Игра не окончена {game_result}")
    for frame in game_frames:
        if frame == "X":
            game_score += 20
        else:
            if frame[0] == "-":
                frame[0] = "0"
            if frame[1] == "-":
                frame[1] = "0"

            if frame[0] == "/":
                raise Exception(f"Некорректная запись в игре {game_result}, во фрейме {frame}")
            elif frame[1] == "/":
                game_score += 15

            elif frame[0] not in "1234567890" or frame[1] not in "1234567890":
                raise Exception(f"Некорректный символ в игре {game_result}, во фрейме {frame}")
            else:
                game_score += int(frame[0]) + int(frame[1])
    # print(f"Игра {game_frames} ---> {game_score} очков")
    return game_score


if __name__ == '__main__':
    list_of_results = game_result_generator()
    for game in list_of_results:
        get_score(game_result=game)
