import threading
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
    lock1 = threading.Lock()
    lock2 = threading.Lock()

    thread1 = threading.Thread(target=task1, args=(lock1, lock2))
    thread2 = threading.Thread(target=task2, args=(lock1, lock2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("All tasks are done!")
