# -*- coding: utf-8 -*-

# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от средней цены за торговую сессию:
#   средняя цена = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / средняя цена) * 100%
# Например для бумаги №1:
#   average_price = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / average_price) * 100 = 8.7%
# Для бумаги №2:
#   average_price = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / average_price) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base_source/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>


import operator
import os
import csv
import time


class TickerHandler:

    START_MAX_DIGIT = 0.00001
    START_MIN_DIGIT = 10000000.00001

    def __init__(self, directory=None):
        self.directory = directory
        self.tickers = {}
        self.zero_tickers = []
        self.slice_max = []
        self.slice_min = []

    def run(self):
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".csv"):
                    filename = root + "\\" + file
                    self.csv_reader(filename)
        self.find_extreme_volatility()

    def csv_reader(self, filename):
        with open(filename, encoding="utf-8") as csv_file:
            max_price = self.START_MAX_DIGIT
            min_price = self.START_MIN_DIGIT
            file_reader = csv.reader(csv_file, delimiter=",")
            for row in file_reader:
                ticker, time, price, quantity = row
                if price == "PRICE":
                    continue
                if float(price) > max_price:
                    max_price = float(price)
                if float(price) < min_price:
                    min_price = float(price)
            average_price = (max_price + min_price) / 2
            volatility = (max_price - min_price) / average_price * 100
            self.tickers[ticker] = round(volatility, 2)

    def find_extreme_volatility(self):
        sorted_tickers = list(sorted(self.tickers.items(), key=operator.itemgetter(1)))
        zero_tickers_count = 0
        for ticker, volatility in sorted_tickers:
            if volatility == 0:
                self.zero_tickers.append(ticker)
                zero_tickers_count += 1
            else:
                break
        sorted_tickers = sorted_tickers[zero_tickers_count:]
        sorted_tickers.sort(key=operator.itemgetter(1), reverse=True)
        self.slice_max = sorted_tickers[0:3]
        self.slice_min = sorted_tickers[-3:]
        self.zero_tickers.sort()

        self.print_results()

    def print_results(self):
        print("Максимальная волатильность:")
        for ticker, volatility in self.slice_max:
            print("\t", ticker, "-", volatility, " %")

        print("Минимальная волатильность:")
        for ticker, volatility in self.slice_min:
            print("\t", ticker, "-", volatility, " %")

        print("Нулевая волатильность:")
        i = 0
        for ticker in self.zero_tickers:
            if i > 0:
                print(f", {ticker}", end="")
            else:
                i += 1
                print(f"\t {ticker}", end="")


started_at = time.time()
Handler = TickerHandler('trades')
Handler.run()
ended_at = time.time()
elapsed = round(ended_at - started_at, 4)
print(f"\n\n")
print(f'Функция работала {elapsed} секунд(ы)')