# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
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


import operator
import os
import csv
from multiprocessing import Process, Queue
import time


class TickerHandler(Process):
    START_MAX_DIGIT = 0.00001
    START_MIN_DIGIT = 10000000.00001

    def __init__(self, directory=None, result_queue=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directory = directory
        self.result_queue = result_queue
        self.tickers = {}
        self.zero_tickers = []
        self.slice_max = []
        self.slice_min = []

    def run(self):
        processes = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".csv"):
                    filename = root + "\\" + file
                    process = Process(target=self.csv_reader, args=(filename,))
                    process.start()
                    processes.append(process)
        for process in processes:
            process.join()
        self.retrieve_results()

    def retrieve_results(self):
        while not self.result_queue.empty():
            ticker, volatility = self.result_queue.get()
            self.tickers[ticker] = volatility
        self.find_extreme_volatility()

    def csv_reader(self, filename):
        with open(filename, encoding="utf-8") as csv_file:
            max_price = self.START_MAX_DIGIT
            min_price = self.START_MIN_DIGIT
            file_reader = csv.reader(csv_file, delimiter=",")
            for row in file_reader:
                ticker, _, price, quantity = row
                if price == "PRICE":
                    continue
                if float(price) > max_price:
                    max_price = float(price)
                if float(price) < min_price:
                    min_price = float(price)
            average_price = (max_price + min_price) / 2
            volatility = (max_price - min_price) / average_price * 100
            self.result_queue.put((ticker, round(volatility, 2)))

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
        if self.zero_tickers:
            print("\t", ", ".join(self.zero_tickers))


if __name__ == '__main__':
    started_at = time.time()
    result_queue = Queue()
    Handler = TickerHandler('trades', result_queue=result_queue)
    # Handler.run() # данная команда приведет к тому, что класс Process "не сработает",
    # параллельный процесс не запустится
    Handler.start()  # при использовании класса multiprocessing.Process, основной метод,
    # который выполняется в созданном процессе, должен называться именно run()
    Handler.join()
    ended_at = time.time()
    elapsed = round(ended_at - started_at, 4)
    print(f"\n\n")
    print(f'Функция работала {elapsed} секунд(ы)')
