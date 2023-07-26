# реализация многозадачности с очередью через класс

import multiprocessing


class PowerCalculator(multiprocessing.Process):
    def __init__(self, number, power, result_queue):
        super().__init__()
        self.number = number
        self.power = power
        self.result_queue = result_queue

    def run(self):
        result = self.number ** self.power
        self.result_queue.put((self.number, self.power, result))


if __name__ == '__main__':
    result_queue = multiprocessing.Queue()
    processes = []
    for i in range(1, 11):  # Создаем 10 экземпляров класса PowerCalculator
        process = PowerCalculator(number=i, power=10, result_queue=result_queue)
        processes.append(process)

    # Запускаем все процессы
    for process in processes:
        process.start()

    # Ожидаем завершения всех процессов
    for process in processes:
        process.join()

    results = []
    while not result_queue.empty():
        result = result_queue.get()
        results.append(result)

    # Выводим результаты каждого процесса
    for number, power, result in results:
        print(f"Number {number}^{power} = {result}")

    print("All processes are done!")
