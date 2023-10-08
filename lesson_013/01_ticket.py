# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

from PIL import Image, ImageDraw, ImageFont, ImageColor
import os

SCALING = 3.5


def make_ticket(fio, from_, to_, date):
    pic_of_ticker = Image.open("images\\ticket_template.png")
    w, h = pic_of_ticker.size
    pic_of_ticker = pic_of_ticker.resize((int(w * SCALING), int(h * SCALING)))

    draw = ImageDraw.Draw(pic_of_ticker)

    font_size = int(20 * SCALING)
    font_size_date = int(15 * SCALING)
    font_path = os.path.join("fonts", "ofont.ru_Manrope.ttf")
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

    pic_of_ticker.save("images\\ticket_sample_result.png")


make_ticket(fio="Terekhov I.A.", from_="NOVOSIBIRSK", to_="BATUMI", date="01.04.23")

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
