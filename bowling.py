from random import randint


def add_mistakes(game_result):
    def wrap(*args, **kwargs):

        maybe_symbols = "XXX///---000123456789ABCDIFG"
        game_results = game_result(*args, **kwargs)
        replace_count = 0
        for frame_number in range(len(game_results)):
            if randint(1, 100) > 90:
                replace_count += 1
                old_frame = game_results[frame_number]
                old_char = randint(0, len(old_frame) - 1)
                new_char = randint(0, len(maybe_symbols) - 1)
                new_frame = old_frame[:old_char] + maybe_symbols[new_char] + old_frame[old_char + 1:]
                game_results[frame_number] = new_frame
        print(f"Всего испорчено {replace_count} фреймов")
        return game_results
    return wrap


@add_mistakes
def game_result_generator():
    skittles = 10
    game_results = []

    for game_no in range(100):
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


def get_score(game_result):
    pass


print(game_result_generator())
