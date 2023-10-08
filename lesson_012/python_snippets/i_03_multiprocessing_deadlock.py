import multiprocessing
import time


def task1(lock1, lock2):
    with lock1:
        print("Task 1 acquired lock 1")
        # Имитация работы
        time.sleep(1)
        with lock2:
            print("Task 1 acquired lock 2")


def task2(lock1, lock2):
    with lock2:
        print("Task 2 acquired lock 2")
        # Имитация работы
        time.sleep(1)
        with lock1:
            print("Task 2 acquired lock 1")


if __name__ == "__main__":
    lock1 = multiprocessing.Lock()
    lock2 = multiprocessing.Lock()

    process1 = multiprocessing.Process(target=task1, args=(lock1, lock2))
    process2 = multiprocessing.Process(target=task2, args=(lock1, lock2))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    print("All tasks are done!")
