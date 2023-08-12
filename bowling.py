from random import randint


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
