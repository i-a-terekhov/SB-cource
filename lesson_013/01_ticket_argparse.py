# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import argparse

SCALING = 3.5

current_script_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_script_path, "images", "ticket_template.png")
font_path = os.path.join(current_script_path, "fonts", "ofont.ru_Manrope.ttf")


def make_ticket(fio, from_, to_, date, save):
    pic_of_ticker = Image.open(image_path)
    w, h = pic_of_ticker.size
    pic_of_ticker = pic_of_ticker.resize((int(w * SCALING), int(h * SCALING)))

    draw = ImageDraw.Draw(pic_of_ticker)

    font_size = int(20 * SCALING)
    font_size_date = int(15 * SCALING)

    font = ImageFont.truetype(font_path, size=font_size)
    font_for_date = ImageFont.truetype(font_path, size=font_size_date)

    w, h = pic_of_ticker.size
    percent_h_name = 0.29
    percent_h_from = 0.46
    percent_h_to = 0.63
    percent_h_date = 0.64
    percent_w_first_column = 0.07
    percent_w_second_column = 0.43

    message = fio
    draw.text((w * percent_w_first_column, h * percent_h_name), message, font=font, fill=ImageColor.colormap['black'])
    message = from_
    draw.text((w * percent_w_first_column, h * percent_h_from), message, font=font, fill=ImageColor.colormap['black'])
    message = to_
    draw.text((w * percent_w_first_column, h * percent_h_to), message, font=font, fill=ImageColor.colormap['black'])
    message = date
    draw.text((w * percent_w_second_column, h * percent_h_date), message, font=font_for_date,
              fill=ImageColor.colormap['black'])

    if save is None:
        image_save_path = os.path.join(current_script_path, "images", "ticket_sample_result.png")
    else:
        image_save_path = os.path.join(save, "ticket_sample_result.png")

    pic_of_ticker.save(image_save_path)


def check(arg):
    # в данной функции можно осуществить проверку на тип данных
    return arg


def main():
    parser = argparse.ArgumentParser(description="Info about user")

    parser.add_argument("-f", "--fio", nargs="?")
    parser.add_argument("-fr", "--from_", nargs="?")
    parser.add_argument("-t", "--to_", nargs="?")
    parser.add_argument("-d", "--date", type=check, nargs="?")
    parser.add_argument("-s", "--save", nargs="?")
    args = parser.parse_args()

    input_fields = ["fio", "from_", "to_", "date"]
    for field in input_fields:
        if getattr(args, field) is None:
            setattr(args, field, input(f"Заполните {field.upper()}: "))

    if args.save is None and input("Желаете изменить директорию сохранения? [Y/N] ") == "Y":
        new_directory_for_save = input("Введите новую директорию: ")
        args.save = new_directory_for_save

    make_ticket(args.fio, args.from_, args.to_, args.date, args.save)


if __name__ == "__main__":
    main()


# Для запуска скрипта выбираем в командной строке директорию локального python
# cd C:\Users\Ivan\PyCharm\SkillBox\lesson_013\venv\Scripts
# и вводим команду с аргументами
# python ../../01_ticket_argparse.py -t 666 -f 444 -d 777 -fr 555
# далее можем указать новый путь для сохранения, например "F:\"


# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
