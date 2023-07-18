# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
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
# TODO Внимание! это задание можно выполнять только после зачета lesson_012/01_volatility.py !!!

# TODO тут ваш код в многопоточном стиле

import operator
import os
import csv
from threading import Thread
import time


class TickerHandler(Thread):
    START_MAX_DIGIT = 0.00001
    START_MIN_DIGIT = 10000000.00001

    def __init__(self, directory=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directory = directory
        self.tickers = {}
        self.zero_tickers = []
        self.slice_max = []
        self.slice_min = []

    def run(self):
        threads = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".csv"):
                    filename = root + "\\" + file
                    thread = Thread(target=self.csv_reader, args=(filename, ))
                    thread.start()
                    threads.append(thread)
        for thread in threads:
            thread.join()
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