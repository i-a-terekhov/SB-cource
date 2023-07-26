# реализация многозадачности с очередью через функцию

import multiprocessing


def power_calculator(number, power, result_queue):
    result = number ** power
    result_queue.put((number, power, result))


if __name__ == '__main__':
    result_queue = multiprocessing.Queue()
    processes = []
    for i in range(1, 11):
        process = multiprocessing.Process(target=power_calculator, args=(i, 10, result_queue,))
        processes.append(process)

    for process in processes:
        process.start()

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
