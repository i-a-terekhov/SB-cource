# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

from PIL import Image, ImageDraw, ImageFont, ImageColor
import os


SCALING = 1.1


def make_ticket(fio, from_, to, date):
    pic_of_ticker = Image.open("images\\ticket_template.png")
    w, h = pic_of_ticker.size
    pic_of_ticker = pic_of_ticker.resize((int(w * SCALING), int(h * SCALING)))

    font_path = os.path.join("fonts", "ofont.ru_Manrope.ttf")
    draw = ImageDraw.Draw(pic_of_ticker)
    font = ImageFont.truetype(font_path, size=26)

    w, h = pic_of_ticker.size
    percent_h_name = 0.28
    percent_h_from = 0.45
    percent_h_to = 0.62
    percent_h_date = 0.62
    percent_w_first_column = 0.07
    percent_w_second_column = 0.43

    message = f"ФИО ПАССАЖИРА"
    draw.text((w * percent_w_first_column, h * percent_h_name), message, font=font, fill=ImageColor.colormap['black'])

    message = f"ОТКУДА"
    draw.text((w * percent_w_first_column, h * percent_h_from), message, font=font, fill=ImageColor.colormap['black'])

    message = f"КУДА"
    draw.text((w * percent_w_first_column, h * percent_h_to), message, font=font, fill=ImageColor.colormap['black'])

    message = f"ДАТА"
    draw.text((w * percent_w_second_column, h * percent_h_date), message, font=font, fill=ImageColor.colormap['black'])


    pic_of_ticker.save("images\\ticket_sample_result.png")


make_ticket(fio="Terekhov I.A.", from_="NOVOSIBIRSK", to="BATUMI", date="01.04.23")

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
